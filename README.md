# Stroke Recovery Program Cards

**Recovery in Motion** — Personalized, accessible rehabilitation exercises that empower patients and caregivers through evidence-based, easy-to-use printed cards.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.7+](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)

## Why SRP Cards?

After stroke, recovery depends on consistent exercise. But accessing rehabilitation is hard: therapists are expensive, transportation is difficult, and patients often have cognitive or vision challenges. Caregivers lack training. Exercise sheets are confusing. Recovery stalls.

**Stroke Recovery Program Cards put evidence-based rehabilitation directly into the hands of patients and caregivers.** Personalized. Accessible. Printable. Low-cost. Works anywhere.

## Features

- **4 Exercise Categories**: Hand (★), Shoulder (●), Arm (■), Leg (▲)
- **Multiple Output Formats**: 4 on 1 page, large single cards, icons only
- **Accessibility First**: Colorblind-safe Okabe-Ito palette, large typography, shape + number ID
- **Three Interfaces**: Browser (caregiver-friendly) + CLI (power users) + **Raspberry Pi display** (always-on HDMI)
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

### Raspberry Pi Display (Always-On)

Turn a Raspberry Pi Zero 2W into a plug-in bedside display that cycles through
the day's exercises on an HDMI monitor — no browser, no printing, no compositor.
One large card at a time, changing every **30 minutes by default** (editable
down to 15-minute steps). Update the program over SSH by editing a JSON file;
the display picks it up within 5 seconds.

```bash
# On a fresh Pi Zero 2W running RPi OS Lite, after SSHing in:
curl -fsSL https://raw.githubusercontent.com/bayanimills/Stroke-Recovery-Program-Cards/main/scripts/install-pi.sh | sudo bash

# Edit the program any time:
sudo nano /etc/srp/program.json
```

Full walkthrough: [docs/DEPLOY.md](docs/DEPLOY.md). Hardware details and
framebuffer troubleshooting: [docs/HARDWARE.md](docs/HARDWARE.md).

## Exercise Library

| Category | Icon | Color | Exercises |
|----------|------|-------|-----------|
| **Hand** | ★ | Blue (#0072B2) | Stress Ball Squeeze, Finger Pinches, Water Bottle Squeeze |
| **Shoulder** | ● | Orange (#E69F00) | Gentle Arm Lift, Clasped Hands, Shoulder Circles |
| **Arm** | ■ | Green (#009E73) | Nose Touch, Elbow Bend, Water Bottle Hold |
| **Leg** | ▲ | Purple (#CC79A7) | Knee to Chest Lift, Seated Leg Raise, Leg Up with Toes |

## Who Is This For?

### Stroke Patients
Clear daily structure. Accessible design that works even with vision or memory challenges. Track progress and build confidence on your own timeline.

### Caregivers
No PT background needed. Generate a personalized exercise routine in 5 minutes. Print it. Laminate it. Your patient does 1-2 cards daily. You track completion.

### Clinical Administrators
Standardize exercise delivery across your facility. Generate customized cards for each patient. Evidence-based, accessible, scalable.

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
├── pyproject.toml            # Package config, CLI + device entry points
├── requirements.txt          # CLI/PDF dependencies (reportlab)
├── requirements-device.txt   # Device dependencies (pygame)
├── index.html                # Root redirect → web/index.html
│
├── srp/
│   └── exercises.py          # Shared exercise library (CLI + device)
│
├── web/
│   ├── index.html            # Caregiver web interface (primary)
│   └── system.html           # Admin documentation
│
├── cli/
│   └── exercise_sheet.py     # Python CLI tool (PDF output)
│
├── device/                    # Raspberry Pi framebuffer display
│   ├── display.py            # Main loop
│   ├── renderer.py           # pygame card drawing
│   ├── config.py             # JSON config loader + mtime watcher
│   └── __main__.py           # `python -m device`
│
├── config/
│   └── program.example.json  # Default device config
│
├── systemd/
│   └── srp-display.service   # Pi systemd unit
│
├── scripts/
│   ├── install-pi.sh         # Idempotent fresh-Pi installer
│   └── update.sh             # Pull latest + restart service
│
├── tests/
│   ├── test_exercise_sheet.py
│   ├── test_web_interface.py
│   └── test_device_renderer.py
│
├── docs/
│   ├── DEPLOY.md             # Pi deployment walkthrough
│   ├── HARDWARE.md           # Framebuffer & Pi hardware notes
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

# Open caregiver interface
open web/index.html
```

## Usage

### Browser Interface

1. Open `web/index.html`
2. Enter patient name and ability level
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
- [ ] Patient progress tracking dashboard
- [ ] Mobile app version
- [ ] Multi-language support
- [ ] Ability-level variants
- [ ] EMR/EHR system integration

## License

MIT License. See [LICENSE](LICENSE) file for details.

## Credits

Designed with an accessibility-first approach for post-stroke rehabilitation.

## FAQ

**Q: Can I add my own exercises?**
A: Currently, you modify the Python script. A web-based editor is on the roadmap.

**Q: Is internet required?**
A: No. Both web interface and CLI work completely offline.

**Q: What if a patient is colorblind?**
A: The Okabe-Ito palette is tested to be distinguishable for all color vision types. The shape + number system provides redundant identification.

**Q: Can I track patient progress?**
A: Laminate the cards and use dry-erase markers for daily goal tracking. Digital progress tracking is on the roadmap.

---

*Professional rehabilitation, accessible to everyone. Generate. Print. Progress.*
