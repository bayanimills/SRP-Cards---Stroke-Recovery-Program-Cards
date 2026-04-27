# Recovery Program Cards

**Self-Driven Recovery in Motion** — Personalized, accessible movement-practice cards that empower individuals and facilitators through easy-to-use printed cards.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.7+](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)

## Why Recovery Program Cards?

Recovery depends on consistent movement practice. But accessing structured guidance is hard: therapists are expensive, transportation is difficult, and individuals often have cognitive or vision challenges. Facilitators lack training. Exercise sheets are confusing. Progress stalls.

**Recovery Program Cards put structured movement practice directly into the hands of individuals and facilitators.** Personalized. Accessible. Printable. Low-cost. Works anywhere.

## Features

- **4 Exercise Categories**: Hand (★), Shoulder (●), Arm (■), Leg (▲)
- **Multiple Output Formats**: 4 on 1 page, large single cards, icons only
- **Accessibility First**: Colorblind-safe Okabe-Ito palette, large typography, shape + number ID
- **Two Interfaces**: Browser (facilitator-friendly) + CLI (power users)
- **Works Offline**: No internet, no subscriptions, no cloud dependency
- **Print & Laminate**: A4 landscape, laminate-friendly for daily goal tracking

## Quick Start

### Browser (No Installation)

1. Visit [bayanimills.github.io/SRP-Cards---Stroke-Recovery-Program-Cards](https://bayanimills.github.io/SRP-Cards---Stroke-Recovery-Program-Cards/web/index.html) or open `web/index.html` locally
2. Create a personalized exercise program in 5 minutes
3. Print, laminate, track progress

### Command Line

```bash
# Install (includes CLI entry point)
pip install -e .

# Generate card set: 4 cards on 1 page
exercise-sheet -1 hand_0 -2 shoulder_1 -3 arm_2 -4 leg_0 -o output.pdf

# Generate large cards: 1 per page (2x size, easier to read)
exercise-sheet -1 hand_0 -2 shoulder_1 -3 arm_2 -4 leg_0 --layout single -o output.pdf
```

## Exercise Library

| Category | Icon | Color | Exercises |
|----------|------|-------|-----------|
| **Hand** | ★ | Blue (#0072B2) | Stress Ball Squeeze, Finger Pinches, Water Bottle Squeeze |
| **Shoulder** | ● | Orange (#E69F00) | Gentle Arm Lift, Clasped Hands, Shoulder Circles |
| **Arm** | ■ | Green (#009E73) | Nose Touch, Elbow Bend, Water Bottle Hold |
| **Leg** | ▲ | Purple (#CC79A7) | Knee to Chest Lift, Seated Leg Raise, Leg Up with Toes |

## Who Is This For?

### Individuals
Clear daily structure. Accessible design that works even with vision or memory challenges. Track progress and build confidence on your own timeline.

### Facilitators (family, friends, support workers)
No training needed. Generate a personalized exercise routine in 5 minutes. Print it. Laminate it. The individual does 1-2 cards daily. You track completion together.

### Program Administrators
Standardize exercise delivery across your facility. Generate customized cards for each individual. Accessible, scalable.

## Design System

- **Colorblind Safe**: Okabe-Ito palette — distinguishable for all color vision types
- **Large Typography**: 24pt steps, 22pt headings, 0.8cm line spacing
- **Shape + Number ID**: ★1, ●2, ■3, ▲4 — instant identification for cognitive accessibility
- **Goal Tracking Box**: 2.2cm box (top-right) with category-matched border for daily checkmarks
- **Laminate Friendly**: Works with dry-erase markers on laminated sheets

## Project Structure

```
srp-cards/
├── README.md                 # This file
├── LICENSE                   # MIT License
├── pyproject.toml            # Package config & CLI entry point
├── requirements.txt          # Python dependencies
├── index.html                # Root redirect → web/index.html
│
├── web/
│   ├── index.html            # Facilitator web interface (primary)
│   └── system.html           # Admin documentation
│
├── cli/
│   └── exercise_sheet.py     # Python CLI tool
│
├── tests/
│   ├── test_exercise_sheet.py
│   └── test_web_interface.py
│
├── docs/
│   ├── GITHUB_SETUP.md       # Setup guide
│   └── QUICK_PUSH.md         # Quick reference
│
├── examples/                  # Sample outputs
│
└── .github/workflows/         # CI & GitHub Pages deployment
```

## Installation

### Prerequisites

- Python 3.7 or higher
- A modern web browser (Chrome, Firefox, Safari, Edge)
- A4 printer (landscape recommended)

### Setup

```bash
git clone https://github.com/bayanimills/SRP-Cards---Stroke-Recovery-Program-Cards.git
cd SRP-Cards---Stroke-Recovery-Program-Cards

# Install package with CLI tool
pip install -e .

# Open facilitator interface
open web/index.html
```

## Usage

### Browser Interface

1. Open `web/index.html`
2. Enter name and ability level
3. Select one exercise per category
4. Choose output format (4-on-1 or large cards)
5. Generate & Print

### CLI Reference

```
-1, --pos1 TYPE_INDEX    Hand exercise (e.g., hand_0)
-2, --pos2 TYPE_INDEX    Shoulder exercise
-3, --pos3 TYPE_INDEX    Arm exercise
-4, --pos4 TYPE_INDEX    Leg exercise
-l, --layout             four (default) or single
-o, --output             Output filename (default: exercise-sheet.pdf)
```

## Printing Guidelines

1. **Color**: Print in color for best accessibility (colorblind-safe palette)
2. **Paper**: A4 landscape orientation
3. **Lamination**: Recommended for durability and daily tracking
4. **Markers**: Use dry-erase markers on laminated sheets for goal tracking

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -m 'Add your feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open a Pull Request

### Roadmap

- [ ] Custom exercise library editor
- [ ] Progress tracking dashboard
- [ ] Mobile app version
- [ ] Multi-language support
- [ ] Ability-level variants
- [ ] EMR/EHR system integration

## License

MIT License. See [LICENSE](LICENSE) file for details.

## Credits

Designed with an accessibility-first approach for self-driven recovery and movement practice.

## FAQ

**Q: Can I add my own exercises?**
A: Currently, you modify the Python script. A web-based editor is on the roadmap.

**Q: Is internet required?**
A: No. Both web interface and CLI work completely offline.

**Q: What if someone is colorblind?**
A: The Okabe-Ito palette is tested to be distinguishable for all color vision types. The shape + number system provides redundant identification.

**Q: Can I track progress?**
A: Laminate the cards and use dry-erase markers for daily goal tracking. Digital progress tracking is on the roadmap.

---

*Accessible movement practice for everyone. Generate. Print. Progress.*
