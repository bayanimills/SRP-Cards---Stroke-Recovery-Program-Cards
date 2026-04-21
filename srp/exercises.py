"""Canonical exercise library — shared by the PDF CLI and the device renderer.

One source of truth. Both `cli/exercise_sheet.py` (prints PDFs) and
`device/` (draws to framebuffer via pygame) import from here.
"""

from __future__ import annotations

CATEGORIES = ("hand", "shoulder", "arm", "leg")

EXERCISES = {
    "hand": {
        "hex": "#0072B2",
        "shape": "★",
        "num": 1,
        "title": "HAND EXERCISES",
        "exercises": [
            {
                "name": "STRESS BALL SQUEEZE",
                "steps": [
                    "1. Hold ball in right hand",
                    "2. Squeeze firmly (count to 3)",
                    "3. Slowly Release",
                ],
            },
            {
                "name": "FINGER PINCHES",
                "steps": [
                    "1. Pinch with thumb & each finger",
                    "2. Hold each for 5 seconds",
                ],
            },
            {
                "name": "WATER BOTTLE SQUEEZE",
                "steps": [
                    "1. Hold 300ml water bottle",
                    "2. Squeeze as hard as you can",
                    "3. Slowly Release",
                ],
            },
        ],
    },
    "shoulder": {
        "hex": "#E69F00",
        "shape": "●",
        "num": 2,
        "title": "SHOULDER EXERCISES",
        "exercises": [
            {
                "name": "GENTLE ARM LIFT",
                "steps": [
                    "1. Extend arm outwards",
                    "2. Elevate to 45 degrees",
                    "3. Hold in place",
                    "4. Lower slowly",
                ],
            },
            {
                "name": "CLASPED HANDS",
                "steps": [
                    "1. Clasp hands together",
                    "2. Slowly Raise to ceiling",
                    "3. Hold in place for 10 seconds",
                    "4. Slowly Lower Arms",
                ],
            },
            {
                "name": "SHOULDER CIRCLES",
                "steps": [
                    "1. Small circular motions",
                    "2. Forward 5 circles",
                    "3. Backward 5 circles",
                    "4. Keep movements slow",
                ],
            },
        ],
    },
    "arm": {
        "hex": "#009E73",
        "shape": "■",
        "num": 3,
        "title": "ARM EXERCISES",
        "exercises": [
            {
                "name": "NOSE TOUCH",
                "steps": [
                    "1. Extend arm out at 45 degrees",
                    "2. Touch nose",
                    "3. Extend straight back out",
                ],
            },
            {
                "name": "ELBOW BEND",
                "steps": [
                    "1. Bend elbow to 90°",
                    "2. Hold 2 seconds",
                    "3. Straighten slowly",
                ],
            },
            {
                "name": "WATER BOTTLE HOLD",
                "steps": [
                    "1. Hold 300ml bottle",
                    "2. Elevate to 30°",
                    "3. Hold in place for 10",
                    "4. Slowly Lower",
                ],
            },
        ],
    },
    "leg": {
        "hex": "#CC79A7",
        "shape": "▲",
        "num": 4,
        "title": "LEG EXERCISES",
        "exercises": [
            {
                "name": "KNEE TO CHEST LIFT",
                "steps": [
                    "1. Lift knee as high as you can",
                    "2. Hold for 2 seconds",
                    "3. Slowly Lower Leg",
                ],
            },
            {
                "name": "SEATED LEG RAISE",
                "steps": [
                    "1. Sit in chair with support",
                    "2. Extend leg straight",
                    "3. Hold in place",
                    "4. Lower slowly",
                ],
            },
            {
                "name": "LEG UP WITH TOES UP AND DOWN",
                "steps": [
                    "1. Lay down on your back",
                    "2. Lift leg up",
                    "3. Move toes up and down",
                    "4. Lower leg slowly",
                ],
            },
        ],
    },
}


def parse_position(pos_str: str) -> tuple[str, int]:
    """Parse a position string like 'hand_0' into ('hand', 0)."""
    if "_" not in pos_str:
        raise ValueError(f"Invalid position format: {pos_str}. Use 'type_index' (e.g., hand_0)")
    parts = pos_str.rsplit("_", 1)
    exercise_type = parts[0]
    try:
        exercise_idx = int(parts[1])
    except ValueError as e:
        raise ValueError(f"Invalid position format: {pos_str}. Index must be a number") from e
    if exercise_type not in EXERCISES:
        raise ValueError(f"Unknown exercise type: {exercise_type}")
    return (exercise_type, exercise_idx)


def get_exercise(exercise_type: str, exercise_idx: int) -> dict:
    """Return the specific exercise dict for a given (type, index)."""
    if exercise_type not in EXERCISES:
        raise ValueError(f"Unknown exercise type: {exercise_type}")
    exercises = EXERCISES[exercise_type]["exercises"]
    clamped = min(exercise_idx, len(exercises) - 1)
    return exercises[clamped]
