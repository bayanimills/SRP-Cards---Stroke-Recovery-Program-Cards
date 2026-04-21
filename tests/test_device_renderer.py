"""Headless smoke tests for the device renderer.

Runs with SDL_VIDEODRIVER=dummy so it can execute in CI or on the dev
workstation with no framebuffer attached.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

pygame = pytest.importorskip("pygame")

from device import config as cfg  # noqa: E402
from device import display  # noqa: E402
from device import renderer  # noqa: E402


@pytest.fixture(autouse=True)
def _pygame_init():
    pygame.display.init()
    pygame.font.init()
    yield
    pygame.font.quit()
    pygame.display.quit()


def test_config_load_defaults(tmp_path: Path):
    missing = tmp_path / "nope.json"
    program = cfg.load(missing)
    assert program.dwell_minutes == 30
    assert program.dwell_seconds == 1800
    assert len(program.program) == 4


def test_config_load_valid(tmp_path: Path):
    path = tmp_path / "p.json"
    path.write_text(
        json.dumps(
            {
                "patient": "Jim",
                "dwell_minutes": 45,
                "program": ["hand_0", "shoulder_1", "arm_2", "leg_0"],
            }
        )
    )
    program = cfg.load(path)
    assert program.patient == "Jim"
    assert program.dwell_minutes == 45
    assert program.dwell_seconds == 45 * 60
    assert program.positions == [("hand", 0), ("shoulder", 1), ("arm", 2), ("leg", 0)]


def test_config_rejects_sub_minimum_dwell(tmp_path: Path):
    path = tmp_path / "p.json"
    path.write_text(json.dumps({"dwell_minutes": 5, "program": ["hand_0"] * 4}))
    with pytest.raises(ValueError, match="at least 15"):
        cfg.load(path)


def test_config_rejects_non_multiple_of_15(tmp_path: Path):
    path = tmp_path / "p.json"
    path.write_text(json.dumps({"dwell_minutes": 20, "program": ["hand_0"] * 4}))
    with pytest.raises(ValueError, match="multiple of 15"):
        cfg.load(path)


def test_config_accepts_15_minute_dwell(tmp_path: Path):
    path = tmp_path / "p.json"
    path.write_text(json.dumps({"dwell_minutes": 15, "program": ["hand_0"] * 4}))
    assert cfg.load(path).dwell_minutes == 15


def test_config_rejects_wrong_program_length(tmp_path: Path):
    path = tmp_path / "p.json"
    path.write_text(json.dumps({"program": ["hand_0", "shoulder_0"]}))
    with pytest.raises(ValueError):
        cfg.load(path)


def test_config_rejects_unknown_exercise(tmp_path: Path):
    path = tmp_path / "p.json"
    path.write_text(json.dumps({"program": ["neck_0", "shoulder_0", "arm_0", "leg_0"]}))
    with pytest.raises(ValueError):
        cfg.load(path)


def test_watcher_detects_change(tmp_path: Path):
    path = tmp_path / "p.json"
    path.write_text("{}")
    watcher = cfg.Watcher(path)
    assert watcher.changed() is False
    # Force mtime forward
    os.utime(path, (path.stat().st_mtime + 5, path.stat().st_mtime + 5))
    assert watcher.changed() is True
    assert watcher.changed() is False


def test_render_single_produces_surface():
    surface = renderer.render_single(1280, 720, "hand", 0, patient="JIM")
    assert surface.get_size() == (1280, 720)


def test_render_message_produces_surface():
    surface = renderer.render_message(1280, 720, "Hello", "detail")
    assert surface.get_size() == (1280, 720)


def test_build_frame_uses_error_when_present():
    surface = display.build_frame(1280, 720, None, "boom", 0)
    assert surface.get_size() == (1280, 720)


def test_build_frame_cycles_through_all_cards(tmp_path: Path):
    path = tmp_path / "p.json"
    path.write_text(
        json.dumps(
            {
                "dwell_minutes": 15,
                "program": ["hand_0", "shoulder_1", "arm_2", "leg_0"],
            }
        )
    )
    program = cfg.load(path)
    for idx in range(4):
        assert display.build_frame(1280, 720, program, None, idx).get_size() == (1280, 720)


def test_run_once_renders_single_frame(tmp_path: Path, monkeypatch):
    path = tmp_path / "p.json"
    path.write_text(
        json.dumps(
            {
                "dwell_minutes": 30,
                "program": ["hand_0", "shoulder_1", "arm_2", "leg_0"],
            }
        )
    )
    monkeypatch.setenv("SRP_RESOLUTION", "640x360")
    rc = display.run(path, once=True)
    assert rc == 0
