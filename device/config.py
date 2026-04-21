"""Config loader + mtime-polling watcher for the device renderer.

The config file is plain JSON, SSH-editable. Example:

  {
    "patient": "Jim",
    "layout": "cycle",
    "dwell_seconds": 30,
    "program": ["hand_0", "shoulder_1", "arm_2", "leg_0"]
  }

`layout` is either "cycle" (one card at a time, default) or "grid"
(4 cards on one screen, static).
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path

from srp.exercises import parse_position

DEFAULT_CONFIG_PATH = Path(os.environ.get("SRP_CONFIG", "/etc/srp/program.json"))

DEFAULT_PROGRAM = ["hand_0", "shoulder_0", "arm_0", "leg_0"]


@dataclass(frozen=True)
class Program:
    patient: str = ""
    layout: str = "cycle"
    dwell_seconds: int = 30
    program: list[str] = field(default_factory=lambda: list(DEFAULT_PROGRAM))

    @property
    def positions(self) -> list[tuple[str, int]]:
        return [parse_position(p) for p in self.program]


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
        layout=str(raw.get("layout", "cycle") or "cycle"),
        dwell_seconds=int(raw.get("dwell_seconds", 30) or 30),
        program=list(raw.get("program", DEFAULT_PROGRAM)) or list(DEFAULT_PROGRAM),
    )
    # Validate every position string up-front.
    _ = program.positions
    if program.layout not in ("cycle", "grid"):
        raise ValueError(f"layout must be 'cycle' or 'grid', got {program.layout!r}")
    if program.dwell_seconds < 1:
        raise ValueError(f"dwell_seconds must be >= 1, got {program.dwell_seconds}")
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
