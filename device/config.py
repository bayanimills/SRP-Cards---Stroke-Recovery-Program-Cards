"""Config loader + mtime-polling watcher for the device renderer.

The config file is plain JSON, SSH-editable. Example:

  {
    "patient": "Jim",
    "dwell_minutes": 30,
    "program": ["hand_0", "shoulder_1", "arm_2", "leg_0"]
  }

`dwell_minutes` is how long each card stays on screen before advancing
to the next. Default is 30 minutes; must be a multiple of 15 (15, 30,
45, 60, …) so the display aligns with a quarter-hour clock.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path

from srp.exercises import parse_position

DEFAULT_CONFIG_PATH = Path(os.environ.get("SRP_CONFIG", "/etc/srp/program.json"))

DEFAULT_PROGRAM = ["hand_0", "shoulder_0", "arm_0", "leg_0"]
DWELL_STEP_MINUTES = 15
DEFAULT_DWELL_MINUTES = 30


@dataclass(frozen=True)
class Program:
    patient: str = ""
    dwell_minutes: int = DEFAULT_DWELL_MINUTES
    program: list[str] = field(default_factory=lambda: list(DEFAULT_PROGRAM))

    @property
    def positions(self) -> list[tuple[str, int]]:
        return [parse_position(p) for p in self.program]

    @property
    def dwell_seconds(self) -> int:
        return self.dwell_minutes * 60


def load(path: Path = DEFAULT_CONFIG_PATH) -> Program:
    """Load a Program from disk. Returns defaults if the file is missing.

    Invalid JSON or invalid exercise references raise ValueError so the
    caller can surface the error on-screen rather than silently showing
    stale content.
    """
    if not path.exists():
        return Program()

    with path.open("r", encoding="utf-8") as fh:
        raw = json.load(fh)

    program = Program(
        patient=str(raw.get("patient", "") or ""),
        dwell_minutes=int(raw.get("dwell_minutes", DEFAULT_DWELL_MINUTES) or DEFAULT_DWELL_MINUTES),
        program=list(raw.get("program", DEFAULT_PROGRAM)) or list(DEFAULT_PROGRAM),
    )
    # Validate every position string up-front.
    _ = program.positions
    if program.dwell_minutes < DWELL_STEP_MINUTES:
        raise ValueError(
            f"dwell_minutes must be at least {DWELL_STEP_MINUTES}, got {program.dwell_minutes}"
        )
    if program.dwell_minutes % DWELL_STEP_MINUTES != 0:
        raise ValueError(
            f"dwell_minutes must be a multiple of {DWELL_STEP_MINUTES}, got {program.dwell_minutes}"
        )
    if len(program.program) != 4:
        raise ValueError(f"program must list exactly 4 exercises, got {len(program.program)}")
    return program


class Watcher:
    """Polls a path's mtime. Call `changed()` each tick; it returns True
    exactly when the file has been modified since the last check.
    """

    def __init__(self, path: Path = DEFAULT_CONFIG_PATH):
        self.path = path
        self._last_mtime: float | None = self._mtime()

    def _mtime(self) -> float | None:
        try:
            return self.path.stat().st_mtime
        except FileNotFoundError:
            return None

    def changed(self) -> bool:
        current = self._mtime()
        if current != self._last_mtime:
            self._last_mtime = current
            return True
        return False
