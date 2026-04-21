"""Pure-pygame renderer for SRP cards.

Mirrors the PDF design system from `cli/exercise_sheet.py`:
Okabe-Ito palette, shape+number icon, title, GOAL box, numbered steps,
"REPEAT until GOAL" footer. Kept in the same visual language so printed
cards and the on-screen cards are instantly recognisable as siblings.

Surfaces are rendered once per config change and blitted each frame.
On a Pi Zero 2W this keeps CPU near idle between redraws.
"""

from __future__ import annotations

import datetime
import math
from dataclasses import dataclass

import pygame

from srp.exercises import EXERCISES, get_exercise

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (204, 204, 204)
BANNER_RULE = (80, 80, 80)


def hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    h = hex_str.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


@dataclass(frozen=True)
class Fonts:
    step: pygame.font.Font
    title: pygame.font.Font
    name: pygame.font.Font
    goal: pygame.font.Font
    icon_num: pygame.font.Font
    footer: pygame.font.Font
    patient: pygame.font.Font


def _pick_font(size: int) -> pygame.font.Font:
    """Pygame default font with a bold-capable fallback.

    `SysFont(None)` returns the default bundled font. `bold=True` works
    against any font and avoids requiring DejaVu to exist on the host.
    """
    return pygame.font.SysFont(None, size)


def build_fonts(scale: float) -> Fonts:
    # scale=1.0 is quadrant-sized; scale≈2.0 is full-screen (single card).
    return Fonts(
        step=pygame.font.SysFont(None, max(14, int(40 * scale))),
        title=pygame.font.SysFont(None, max(14, int(38 * scale)), bold=True),
        name=pygame.font.SysFont(None, max(12, int(30 * scale)), bold=True),
        goal=pygame.font.SysFont(None, max(14, int(40 * scale)), bold=True),
        icon_num=pygame.font.SysFont(None, max(20, int(56 * scale)), bold=True),
        footer=pygame.font.SysFont(None, max(14, int(40 * scale)), bold=True),
        patient=pygame.font.SysFont(None, max(12, int(24 * scale)), bold=True),
    )


def _draw_star(surface: pygame.Surface, cx: int, cy: int, outer_r: int, fill: tuple[int, int, int]) -> None:
    inner_r = outer_r // 2
    points = []
    for i in range(10):
        angle = -math.pi / 2 + (i * math.pi / 5)
        r = outer_r if i % 2 == 0 else inner_r
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    pygame.draw.polygon(surface, fill, points)
    pygame.draw.polygon(surface, BLACK, points, max(2, outer_r // 20))


def _draw_icon(surface: pygame.Surface, shape: str, x: int, y: int, size: int, fill: tuple[int, int, int]) -> None:
    rect = pygame.Rect(x, y, size, size)
    if shape == "●":
        pygame.draw.circle(surface, fill, rect.center, size // 2)
        pygame.draw.circle(surface, BLACK, rect.center, size // 2, max(2, size // 24))
    elif shape == "■":
        pygame.draw.rect(surface, fill, rect)
        pygame.draw.rect(surface, BLACK, rect, max(2, size // 24))
    elif shape == "▲":
        points = [
            (rect.centerx, rect.top),
            (rect.right, rect.bottom),
            (rect.left, rect.bottom),
        ]
        pygame.draw.polygon(surface, fill, points)
        pygame.draw.polygon(surface, BLACK, points, max(2, size // 24))
    elif shape == "★":
        _draw_star(surface, rect.centerx, rect.centery, size // 2, fill)


def _draw_card(
    surface: pygame.Surface,
    rect: pygame.Rect,
    exercise_type: str,
    exercise_idx: int,
    fonts: Fonts,
) -> None:
    data = EXERCISES[exercise_type]
    exercise = get_exercise(exercise_type, exercise_idx)
    colour = hex_to_rgb(data["hex"])

    margin = max(10, rect.width // 32)

    icon_size = max(40, int(rect.height * 0.18))
    icon_x = rect.left + margin
    icon_y = rect.top + margin
    _draw_icon(surface, data["shape"], icon_x, icon_y, icon_size, colour)

    # Number centred over the icon
    num_surface = fonts.icon_num.render(str(data["num"]), True, WHITE)
    num_rect = num_surface.get_rect(center=(icon_x + icon_size // 2, icon_y + icon_size // 2))
    # Triangle has a visually-lower centroid; nudge the number down for ▲.
    if data["shape"] == "▲":
        num_rect.move_ip(0, icon_size // 8)
    surface.blit(num_surface, num_rect)

    # Category title (right of icon)
    title_surf = fonts.title.render(data["title"], True, colour)
    title_x = icon_x + icon_size + margin
    title_y = icon_y
    surface.blit(title_surf, (title_x, title_y))

    # Specific exercise name, one line under the title
    name_surf = fonts.name.render(exercise["name"], True, BLACK)
    name_y = title_y + title_surf.get_height() + margin // 2
    surface.blit(name_surf, (title_x, name_y))

    # GOAL label + box, top-right
    goal_box_size = max(60, int(icon_size * 1.2))
    goal_box_x = rect.right - goal_box_size - margin
    goal_box_y = name_y
    goal_surf = fonts.goal.render("GOAL", True, colour)
    surface.blit(
        goal_surf,
        (goal_box_x + goal_box_size // 2 - goal_surf.get_width() // 2, goal_box_y - goal_surf.get_height() - 4),
    )
    pygame.draw.rect(
        surface,
        colour,
        pygame.Rect(goal_box_x, goal_box_y, goal_box_size, goal_box_size),
        max(3, goal_box_size // 20),
    )

    # Steps, stacked
    step_x = rect.left + margin
    step_y = name_y + name_surf.get_height() + margin
    line_h = fonts.step.get_linesize()
    for step in exercise["steps"]:
        step_surf = fonts.step.render(step, True, BLACK)
        surface.blit(step_surf, (step_x, step_y))
        step_y += line_h

    # Footer
    footer_surf = fonts.footer.render("REPEAT until GOAL", True, colour)
    footer_y = rect.bottom - footer_surf.get_height() - margin
    surface.blit(footer_surf, (step_x, footer_y))


def _draw_date_banner(surface: pygame.Surface, width: int, height: int, when: datetime.date) -> None:
    """Draw a date banner at the top of the screen. Format: "MON, 21 APR"."""
    pygame.draw.rect(surface, WHITE, pygame.Rect(0, 0, width, height))
    pygame.draw.line(surface, BANNER_RULE, (0, height - 1), (width, height - 1), 2)
    font = pygame.font.SysFont(None, max(24, int(height * 0.7)), bold=True)
    text = when.strftime("%a, %d %b").upper()
    text_surf = font.render(text, True, BLACK)
    surface.blit(text_surf, text_surf.get_rect(center=(width // 2, height // 2)))


def render_single(
    width: int,
    height: int,
    exercise_type: str,
    exercise_idx: int,
    patient: str = "",
    when: datetime.date | None = None,
) -> pygame.Surface:
    """One card filling the screen — stroke-patient-friendly large format."""
    surface = pygame.Surface((width, height))
    surface.fill(WHITE)

    banner_h = max(48, height // 12)
    _draw_date_banner(surface, width, banner_h, when or datetime.date.today())

    card_rect = pygame.Rect(0, banner_h, width, height - banner_h)
    fonts = build_fonts(scale=2.0)
    _draw_card(surface, card_rect, exercise_type, exercise_idx, fonts)

    if patient:
        label = build_fonts(1.0).patient.render(patient.upper(), True, GREY)
        surface.blit(label, (8, height - label.get_height() - 4))
    return surface


def render_message(width: int, height: int, title: str, detail: str = "") -> pygame.Surface:
    """Full-screen message card — used for config errors or boot messages."""
    surface = pygame.Surface((width, height))
    surface.fill(BLACK)
    font_title = pygame.font.SysFont(None, max(32, height // 12), bold=True)
    font_detail = pygame.font.SysFont(None, max(20, height // 24))
    t_surf = font_title.render(title, True, WHITE)
    surface.blit(t_surf, t_surf.get_rect(center=(width // 2, height // 2 - 40)))
    if detail:
        d_surf = font_detail.render(detail, True, (180, 180, 180))
        surface.blit(d_surf, d_surf.get_rect(center=(width // 2, height // 2 + 30)))
    return surface
