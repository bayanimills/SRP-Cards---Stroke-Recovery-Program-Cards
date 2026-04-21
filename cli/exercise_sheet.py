#!/usr/bin/env python3
"""
Stroke Recovery Program Cards — CLI Generator
Generate personalized, accessible A4 exercise cards for post-stroke rehabilitation
"""

import argparse
import math
import sys

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

from srp.exercises import EXERCISES, parse_position


def draw_star(c, x, y, size, color_hex, scale=1.0):
    """Draw a 5-point star"""
    c.setFillColor(HexColor(color_hex))
    c.setStrokeColor(HexColor("#000000"))
    c.setLineWidth(0.08*cm * scale)

    points = []
    for i in range(10):
        angle = math.pi / 2 + (i * math.pi / 5)
        if i % 2 == 0:
            r = size / 2
        else:
            r = size / 4
        px = x + r * math.cos(angle)
        py = y + r * math.sin(angle)
        points.append((px, py))

    path = c.beginPath()
    path.moveTo(points[0][0], points[0][1])
    for i in range(1, len(points)):
        path.lineTo(points[i][0], points[i][1])
    path.close()
    c.drawPath(path, fill=1, stroke=1)

def draw_shape(c, shape, x, y, size, color_hex, scale=1.0):
    """Draw the appropriate shape with outline"""
    c.setFillColor(HexColor(color_hex))
    c.setStrokeColor(HexColor("#000000"))
    c.setLineWidth(0.08*cm * scale)

    if shape == '●':
        c.circle(x + size/2, y + size/2, size/2, fill=1, stroke=1)
    elif shape == '■':
        c.rect(x, y, size, size, fill=1, stroke=1)
    elif shape == '▲':
        path = c.beginPath()
        path.moveTo(x + size/2, y + size)
        path.lineTo(x, y)
        path.lineTo(x + size, y)
        path.close()
        c.drawPath(path, fill=1, stroke=1)
    elif shape == '★':
        draw_star(c, x + size/2, y + size/2, size, color_hex, scale)

def draw_quadrant_card(c, x_start, y_start, quad_width, quad_height, exercise_type, exercise_idx=0, scale=1.0):
    """Draw a single exercise card in a quadrant

    scale: 1.0 = normal (quadrant size), 2.0 = full A4 page
    """

    if exercise_type not in EXERCISES:
        return

    exercise_data = EXERCISES[exercise_type]
    exercise = exercise_data['exercises'][min(exercise_idx, len(exercise_data['exercises'])-1)]

    margin = 0.4*cm * scale
    content_left = x_start + margin
    content_top = y_start + quad_height - margin

    # Icon (shape) at top-left
    icon_size = 1.8*cm * scale
    icon_x = content_left
    icon_y = content_top - icon_size
    draw_shape(c, exercise_data['shape'], icon_x, icon_y, icon_size, exercise_data['hex'], scale)

    # Number inside icon - adjusted offset for triangle
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", int(28 * scale))
    y_offset = (-0.5*cm if exercise_data['shape'] == '▲' else -0.35*cm) * scale
    c.drawCentredString(icon_x + icon_size/2, icon_y + icon_size/2 + y_offset, str(exercise_data['num']))

    # Title at top left, GOAL label at top right
    title_y = content_top - 0.5*cm * scale

    c.setFont("Helvetica-Bold", int(22 * scale))
    c.setFillColor(HexColor(exercise_data['hex']))
    c.drawString(content_left + icon_size + 0.4*cm*scale, title_y, exercise_data['title'])

    # GOAL label - same line as title
    c.setFont("Helvetica-Bold", int(24 * scale))
    c.setFillColor(HexColor(exercise_data['hex']))
    goal_label_x = x_start + quad_width - 1.5*cm*scale
    c.drawCentredString(goal_label_x, title_y, "GOAL")

    # Exercise name (specific exercise)
    exercise_name_y = content_top - 1.2*cm*scale
    c.setFont("Helvetica-Bold", int(18 * scale))
    c.setFillColor(HexColor("#000000"))
    c.drawString(content_left + icon_size + 0.4*cm*scale, exercise_name_y, exercise['name'])

    # Goal box - top of box aligned with specific exercise name text
    box_size = 2.2*cm * scale
    box_x = x_start + quad_width - box_size - margin

    c.setLineWidth(0.12*cm * scale)
    c.setStrokeColor(HexColor(exercise_data['hex']))
    c.rect(box_x, exercise_name_y - box_size, box_size, box_size, fill=0, stroke=1)

    # Steps - positioned near bottom
    step_font_size = int(24 * scale)
    step_left = x_start + margin
    line_spacing = 0.8*cm * scale

    c.setFont("Helvetica", step_font_size)
    c.setFillColor(HexColor("#000000"))

    repeat_y = y_start + 0.5*cm * scale
    y_pos = repeat_y + (len(exercise['steps']) * line_spacing) + 0.6*cm*scale

    for step in exercise['steps']:
        c.drawString(step_left, y_pos, step)
        y_pos -= line_spacing

    # Final REPEAT instruction at bottom - colored to match category
    c.setFont("Helvetica-Bold", step_font_size)
    c.setFillColor(HexColor(exercise_data['hex']))
    c.drawString(step_left, repeat_y, "REPEAT until GOAL")

def generate_sheet(output_file, pos1, pos2, pos3, pos4, layout='four'):
    """Generate PDF with exercise cards

    layout: 'four' = 4 cards per page, 'single' = 1 card per page (4 pages total, 300% larger)
    """

    if layout == 'single':
        # Generate 4 separate pages - full A4 so card scales up relative to quadrant
        c = canvas.Canvas(output_file, pagesize=landscape(A4))
        width, height = landscape(A4)

        positions = [
            (pos1, "1"),
            (pos2, "2"),
            (pos3, "3"),
            (pos4, "4")
        ]

        for idx, ((exercise_type, exercise_idx), card_num) in enumerate(positions):
            if idx > 0:
                c.showPage()

            c.setFillColor(HexColor("#FFFFFF"))
            c.rect(0, 0, width, height, fill=1, stroke=0)

            # Draw card at full page scale (2.0x quadrant size)
            draw_quadrant_card(c, 0, 0, width, height, exercise_type, exercise_idx, scale=2.0)

        c.save()
    else:
        # Generate 4 cards on one page (original layout)
        c = canvas.Canvas(output_file, pagesize=landscape(A4))
        width, height = landscape(A4)

        c.setFillColor(HexColor("#FFFFFF"))
        c.rect(0, 0, width, height, fill=1, stroke=0)

        quad_width = width / 2
        quad_height = height / 2

        # Draw grid lines
        c.setLineWidth(0.5)
        c.setStrokeColor(HexColor("#CCCCCC"))
        c.line(quad_width, 0, quad_width, height)
        c.line(0, quad_height, width, quad_height)

        # Draw quadrants
        positions = [
            (pos1, 0, quad_height),
            (pos2, quad_width, quad_height),
            (pos3, 0, 0),
            (pos4, quad_width, 0)
        ]

        for (exercise_type, exercise_idx), x, y in positions:
            draw_quadrant_card(c, x, y, quad_width, quad_height, exercise_type, exercise_idx, scale=1.0)

        c.save()

def main():
    parser = argparse.ArgumentParser(
        description='Stroke Recovery Program Cards — Generate personalized rehabilitation exercise cards',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  exercise-sheet --pos1 hand_0 --pos2 shoulder_1 --pos3 arm_2 --pos4 leg_0
  exercise-sheet -1 hand_0 -2 shoulder_1 -3 arm_2 -4 leg_0 --layout single
  exercise-sheet -1 hand_1 -2 shoulder_0 -3 arm_1 -4 leg_2 -o my-exercises.pdf

Layout options:
  --layout four   = 4 cards on 1 A4 landscape page (default)
  --layout single = 1 card per page (4 pages total)

Available exercises:
  hand:     0=Stress Ball, 1=Finger Pinches, 2=Water Bottle
  shoulder: 0=Gentle Arm Lift, 1=Clasped Hands, 2=Shoulder Circles
  arm:      0=Nose Touch, 1=Elbow Bend, 2=Water Bottle Hold
  leg:      0=Knee to Chest, 1=Seated Leg Raise, 2=Leg Up/Toes
        '''
    )

    parser.add_argument('-1', '--pos1', required=True,
                        help='Top-left position (format: type_index, e.g., hand_0)')
    parser.add_argument('-2', '--pos2', required=True,
                        help='Top-right position (format: type_index, e.g., shoulder_1)')
    parser.add_argument('-3', '--pos3', required=True,
                        help='Bottom-left position (format: type_index, e.g., arm_2)')
    parser.add_argument('-4', '--pos4', required=True,
                        help='Bottom-right position (format: type_index, e.g., leg_0)')
    parser.add_argument('-o', '--output',
                        help='Output PDF filename (default: exercise-sheet.pdf)')
    parser.add_argument('-l', '--layout', choices=['four', 'single'], default='four',
                        help='Layout: four=4 cards on 1 page, single=1 card per page (default: four)')

    args = parser.parse_args()

    # Parse positions
    try:
        pos1 = parse_position(args.pos1)
        pos2 = parse_position(args.pos2)
        pos3 = parse_position(args.pos3)
        pos4 = parse_position(args.pos4)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Determine output filename
    output_file = args.output or 'exercise-sheet.pdf'

    # Generate PDF
    try:
        generate_sheet(output_file, pos1, pos2, pos3, pos4, layout=args.layout)
        pages = '4 pages' if args.layout == 'single' else '1 page'
        print(f"✓ Generated: {output_file} ({pages})")
    except Exception as e:
        print(f"Error generating PDF: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
