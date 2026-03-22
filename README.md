# ExerciseFlow

Personalized rehabilitation exercise sheet generator for elderly patients with cognitive and vision impairment.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.7+](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)

## Overview

ExerciseFlow generates customized, accessible exercise instruction sheets for rehabilitation therapy. Designed specifically for elderly patients and caregivers, it combines:

- **Colorblind-safe design** (Okabe-Ito palette)
- **Large, readable text** for low vision
- **Shape + number identification** for cognitive accessibility
- **Multiple output formats** (single page, multi-page, icon-only)
- **Zero dependencies** for web interface (pure HTML/JS)
- **Works completely offline**

## Features

✅ **4 Exercise Categories**: Hand (★), Shoulder (●), Arm (■), Leg (▲)  
✅ **Multiple Output Formats**: Quadrant (4 on 1), Large Cards (1 per page), Icons Only  
✅ **Accessibility First**: Tested for colorblindness, large typography, clear visual hierarchy  
✅ **Two Interfaces**: Browser (caregiver-friendly) + CLI (power users)  
✅ **Offline Capable**: No internet required after download  
✅ **Printable**: Designed for A4 landscape, laminate-friendly  

## Quick Start

### 🌐 Browser (No Installation)

1. Download `web/caregiver-app.html`
2. Open in any web browser
3. Create sheets immediately

**Live demo**: https://username.github.io/exerciseflow/web/caregiver-app.html

### 💻 Command Line

```bash
# Install dependencies
pip install -r requirements.txt

# Generate sheet: 4 cards on 1 page
python3 cli/exercise-sheet -1 hand_0 -2 shoulder_1 -3 arm_2 -4 leg_0 -o output.pdf

# Generate sheet: Large cards (1 per page, 2x size)
python3 cli/exercise-sheet -1 hand_0 -2 shoulder_1 -3 arm_2 -4 leg_0 --layout single -o output.pdf
```

## Exercise Library

| Category | Icon | Color | Exercises |
|----------|------|-------|-----------|
| **Hand** | ★ | Blue (#0072B2) | Stress Ball Squeeze, Finger Pinches, Water Bottle Squeeze |
| **Shoulder** | ● | Orange (#E69F00) | Gentle Arm Lift, Clasped Hands, Shoulder Circles |
| **Arm** | ■ | Green (#009E73) | Nose Touch, Elbow Bend, Water Bottle Hold |
| **Leg** | ▲ | Purple (#CC79A7) | Knee to Chest Lift, Seated Leg Raise, Leg Up with Toes |

## Design System

### Accessibility Features

- **Colorblind Safe**: Uses Okabe-Ito palette (distinguishable for all color vision types)
- **Typography**: 24pt steps, 22pt headings, 0.8cm line spacing
- **Visual Hierarchy**: Bold shape + number (★1, ●2, ■3, ▲4) for instant identification
- **Goal Tracking**: 2.2cm box (top-right) with category-matched border for daily checkmarks
- **Laminate Friendly**: Works with whiteboard markers on laminated sheets

### Target Users

- Elderly patients (65+) with vision or cognitive impairment
- Post-stroke rehabilitation
- Physical therapy compliance tracking
- Home care coordination
- Care facility group sessions

## Project Structure

```
exerciseflow/
├── README.md                 # This file
├── LICENSE                   # MIT License
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
│
├── cli/
│   └── exercise-sheet       # Python CLI tool (executable)
│
├── web/
│   ├── caregiver-app.html   # Consumer-facing interface
│   ├── system.html          # Admin/documentation interface
│   └── index.html           # Developer tool
│
├── docs/
│   ├── DEPLOYMENT.md        # Deployment guide
│   ├── DESIGN.md            # Design system & accessibility
│   └── API.md               # CLI API reference
│
└── examples/
    └── sample-output.pdf    # Example generated PDF
```

## Installation

### Prerequisites

- Python 3.7 or higher
- A modern web browser (Chrome, Firefox, Safari, Edge)
- A4 printer (landscape recommended)

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/exerciseflow.git
cd exerciseflow

# Install Python dependencies
pip install -r requirements.txt

# Make CLI executable (Linux/Mac)
chmod +x cli/exercise-sheet

# Open browser interface
open web/caregiver-app.html
# or
python3 -m http.server 8000  # Then visit http://localhost:8000/web/caregiver-app.html
```

## Usage Examples

### Browser Interface

1. Open `web/caregiver-app.html` in browser
2. Click "Create Sheet"
3. Enter patient name and ability level
4. Select one exercise per category
5. Choose output format
6. Click "Generate & Print"

### CLI Examples

```bash
# Default: 4 cards on 1 A4 page
python3 cli/exercise-sheet -1 hand_0 -2 shoulder_1 -3 arm_2 -4 leg_0

# Single card format: 1 card per page, 4 pages total
python3 cli/exercise-sheet -1 hand_0 -2 shoulder_1 -3 arm_2 -4 leg_0 --layout single

# Custom filename
python3 cli/exercise-sheet -1 hand_1 -2 shoulder_0 -3 arm_2 -4 leg_1 -o patient-john.pdf

# Help
python3 cli/exercise-sheet --help
```

### Argument Reference

```
-1, --pos1 TYPE_INDEX    Hand exercise (type_index format, e.g., hand_0)
-2, --pos2 TYPE_INDEX    Shoulder exercise
-3, --pos3 TYPE_INDEX    Arm exercise
-4, --pos4 TYPE_INDEX    Leg exercise
-l, --layout             four (default) or single
-o, --output             Output filename (default: exercise-sheet.pdf)
```

## Printing Guidelines

1. **Color**: Print in color for best accessibility (colorblind-safe palette)
2. **Paper**: A4 landscape orientation
3. **Lamination**: Optional but recommended for durability
4. **Markers**: Use dry-erase markers on laminated sheets for goal tracking

## Documentation

- [📋 Deployment Guide](docs/DEPLOYMENT.md) - Installation and deployment instructions
- [🎨 Design System](docs/DESIGN.md) - Accessibility features and design rationale
- [🔧 API Reference](docs/API.md) - CLI tool documentation

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Areas for Contribution

- [ ] Custom exercise library editor
- [ ] Patient progress tracking dashboard
- [ ] Mobile app version (React Native)
- [ ] Multi-language support
- [ ] Ability-level variants
- [ ] EMR system integration
- [ ] Accessibility testing

## Roadmap

- **v1.1** - Custom exercise library, patient profiles
- **v1.2** - Progress tracking, calendar integration
- **v2.0** - Mobile app, multi-language support
- **v2.5** - EMR/EHR integrations

## License

MIT License © 2026 P&L Dwyer Engineering. See [LICENSE](LICENSE) file for details.

## Credits

Built by **P&L Dwyer Engineering** in partnership with **Australian Bitcoin Industry Body (ABIB)**.

Designed with accessibility-first approach for elderly rehabilitation.

## Support

- 📖 [Full Documentation](docs/)
- 🐛 [Report Issues](https://github.com/yourusername/exerciseflow/issues)
- 💬 [Discussions](https://github.com/yourusername/exerciseflow/discussions)

## FAQ

**Q: Can I add my own exercises?**  
A: Currently, you modify the Python script. Future version will have web-based editor.

**Q: Is internet required?**  
A: No. Both web interface and CLI work completely offline.

**Q: Can I use this with patients?**  
A: Yes. Designed specifically for patient use. Print and laminate for durability.

**Q: What if a patient is colorblind?**  
A: The palette (Okabe-Ito) is tested to be distinguishable for all color vision types.

**Q: Can I track patient progress?**  
A: Currently sheets are static. Progress tracking is on the roadmap.

---

**Made with ❤️ for elderly rehabilitation**