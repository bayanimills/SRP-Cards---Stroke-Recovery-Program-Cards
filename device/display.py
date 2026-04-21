"""Main display loop for the SRP device renderer.

Responsibilities:
  * Initialise pygame against the framebuffer (or a given SDL driver).
  * Load config, redraw when the config file changes.
  * Cycle single-card layout, or render a static grid.
  * Run forever; signals cleanly shut pygame down so systemd can restart us.
"""

from __future__ import annotations

import logging
import os
import signal
import sys
import time
from pathlib import Path

import pygame

from device import config as cfg
from device import renderer

log = logging.getLogger("srp.display")

DEFAULT_RESOLUTION = (1280, 720)
FRAME_SLEEP = 0.2  # 5 Hz poll — plenty for static cards, negligible CPU.


def detect_resolution() -> tuple[int, int]:
    """Auto-detect framebuffer size from /sys. Fall back to 1280x720."""
    env = os.environ.get("SRP_RESOLUTION")
    if env and "x" in env:
        try:
            w, h = env.lower().split("x", 1)
            return int(w), int(h)
        except ValueError:
            log.warning("SRP_RESOLUTION=%r unparseable; ignoring", env)

    fb = Path("/sys/class/graphics/fb0/virtual_size")
    if fb.exists():
        try:
            raw = fb.read_text().strip()
            w, h = raw.split(",", 1)
            return int(w), int(h)
        except (ValueError, OSError) as e:
            log.warning("Failed to read %s: %s", fb, e)
    return DEFAULT_RESOLUTION


def init_pygame(resolution: tuple[int, int]) -> pygame.Surface:
    """Initialise pygame and return the display surface.

    Honours SDL_VIDEODRIVER / SDL_FBDEV if they're set in the environment
    (the systemd unit sets them). We never touch audio — Pi Zero 2W has
    no built-in audio and initialising it can hang on headless boots.
    """
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
    pygame.display.init()
    pygame.font.init()
    pygame.mouse.set_visible(False)
    # FULLSCREEN + NOFRAME = take the whole framebuffer.
    flags = pygame.FULLSCREEN | pygame.NOFRAME
    if os.environ.get("SDL_VIDEODRIVER") == "dummy":
        flags = 0
    return pygame.display.set_mode(resolution, flags)


def run(config_path: Path = cfg.DEFAULT_CONFIG_PATH, once: bool = False) -> int:
    """Main loop. `once=True` renders a single frame and returns (used by tests)."""
    width, height = detect_resolution()
    log.info("resolution=%sx%s config=%s", width, height, config_path)

    screen = init_pygame((width, height))

    watcher = cfg.Watcher(config_path)
    program: cfg.Program | None = None
    error_message: str | None = None
    frame_surface: pygame.Surface | None = None
    card_idx = 0
    card_shown_at = time.monotonic()

    def reload() -> None:
        nonlocal program, error_message, frame_surface, card_idx, card_shown_at
        try:
            program = cfg.load(config_path)
            error_message = None
            log.info("loaded program: patient=%r layout=%s dwell=%ss program=%s",
                     program.patient, program.layout, program.dwell_seconds, program.program)
        except (ValueError, OSError) as e:
            program = None
            error_message = str(e)
            log.error("config error: %s", e)
        card_idx = 0
        card_shown_at = time.monotonic()
        frame_surface = build_frame(width, height, program, error_message, card_idx)

    reload()

    def _shutdown(signum: int, _frame) -> None:  # noqa: ANN001
        log.info("caught signal %s — shutting down", signum)
        pygame.quit()
        sys.exit(0)

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    while True:
        if watcher.changed():
            log.info("config changed — reloading")
            reload()

        now = time.monotonic()
        if program and program.layout == "cycle":
            if now - card_shown_at >= program.dwell_seconds:
                card_idx = (card_idx + 1) % len(program.positions)
                card_shown_at = now
                frame_surface = build_frame(width, height, program, error_message, card_idx)

        if frame_surface is not None:
            screen.blit(frame_surface, (0, 0))
            pygame.display.flip()

        # Drain events so pygame doesn't backlog (we don't act on them).
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0

        if once:
            pygame.quit()
            return 0

        time.sleep(FRAME_SLEEP)


def build_frame(
    width: int,
    height: int,
    program: cfg.Program | None,
    error_message: str | None,
    card_idx: int,
) -> pygame.Surface:
    if error_message:
        return renderer.render_message(width, height, "Config error", error_message)
    if program is None:
        return renderer.render_message(width, height, "SRP Cards", "No config found — see /etc/srp/program.json")

    positions = program.positions
    if program.layout == "grid":
        return renderer.render_grid(width, height, positions, patient=program.patient)

    etype, eidx = positions[card_idx % len(positions)]
    return renderer.render_single(width, height, etype, eidx, patient=program.patient)


def main() -> int:
    logging.basicConfig(
        level=os.environ.get("SRP_LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    path = Path(os.environ.get("SRP_CONFIG", str(cfg.DEFAULT_CONFIG_PATH)))
    return run(path)


if __name__ == "__main__":
    sys.exit(main())
