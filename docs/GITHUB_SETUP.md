# GitHub Setup Guide - ExerciseFlow

## Quick Start (5 minutes)

### 1. Create Repository on GitHub
```bash
# Go to github.com/new
# Repository name: exerciseflow
# Description: Personalized rehabilitation exercise sheet generator
# Public/Private: Your choice
# Initialize with: README (NO - we'll create our own)
```

### 2. Clone & Setup Locally
```bash
# Create local directory
mkdir exerciseflow && cd exerciseflow

# Initialize git
git init
git config user.name "Your Name"
git config user.email "your@email.com"

# Add remote (replace USERNAME)
git remote add origin https://github.com/USERNAME/exerciseflow.git
git branch -M main
```

### 3. Create Project Structure
```
exerciseflow/
├── README.md
├── .gitignore
├── LICENSE
├── requirements.txt
├── cli/
│   └── exercise-sheet
├── web/
│   ├── caregiver-app.html
│   ├── system.html
│   └── index.html
├── docs/
│   ├── DEPLOYMENT.md
│   ├── DESIGN.md
│   └── API.md
├── tests/
│   └── test_exercises.py
└── examples/
    └── sample-output.pdf
```

### 4. Copy Files
```bash
# From /mnt/user-data/outputs/, organize into structure:
cp exercise-sheet cli/
cp caregiver-app.html web/
cp system.html web/
cp index.html web/
chmod +x cli/exercise-sheet
```

### 5. Create .gitignore
```
# Python
__pycache__/
*.py[cod]
*.egg-info/
*.dist-info/
venv/

# PDFs (don't version control generated files)
*.pdf

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp

# Environment
.env
.env.local
```

### 6. Create requirements.txt
```
reportlab==4.0.7
```

### 7. Create README.md (see template below)

### 8. Push to GitHub
```bash
git add .
git commit -m "Initial commit: ExerciseFlow rehabilitation exercise generator"
git push -u origin main
```

---

## README.md Template

```markdown
# ExerciseFlow

Personalized rehabilitation exercise sheet generator for elderly patients with cognitive and vision impairment.

![License](https://img.shields.io/badge/license-MIT-green)

## Features

- 🎯 **4 Exercise Categories**: Hand, Shoulder, Arm, Leg
- 🖨️ **Multiple Formats**: Single page, quadrant layout, icon sheets
- ♿ **Accessibility**: Colorblind-safe palette, large text, shape+number ID system
- 👥 **Caregiver-Friendly**: Web interface for non-technical users
- 📱 **Offline**: Works completely offline
- 🖥️ **CLI & Web**: Both command-line and browser-based interfaces

## Quick Start

### Web Version (No Installation)
1. Download `web/caregiver-app.html`
2. Open in any browser
3. Create patient sheets instantly

### CLI Version (Requires Python)
```bash
pip install -r requirements.txt

python3 cli/exercise-sheet -1 hand_0 -2 shoulder_1 -3 arm_2 -4 leg_0 -o output.pdf
```

## Usage

### Browser
- **Caregiver Interface**: `web/caregiver-app.html` - User-friendly patient sheet creator
- **System Admin**: `web/system.html` - Full documentation & deployment guide
- **Developer Tool**: `web/index.html` - Advanced exercise selector

### Command Line
```bash
# 4 cards on 1 A4 page
python3 cli/exercise-sheet -1 hand_0 -2 shoulder_1 -3 arm_2 -4 leg_0

# Large cards (2x scaled), 1 per page
python3 cli/exercise-sheet -1 hand_0 -2 shoulder_1 -3 arm_2 -4 leg_0 --layout single

# Custom output filename
python3 cli/exercise-sheet -1 hand_0 -2 shoulder_1 -3 arm_2 -4 leg_0 -o patient-john.pdf
```

## Exercises

| Category | Icon | Exercises |
|----------|------|-----------|
| Hand (Blue) | ★ | Stress Ball Squeeze, Finger Pinches, Water Bottle Squeeze |
| Shoulder (Orange) | ● | Gentle Arm Lift, Clasped Hands, Shoulder Circles |
| Arm (Green) | ■ | Nose Touch, Elbow Bend, Water Bottle Hold |
| Leg (Purple) | ▲ | Knee to Chest Lift, Seated Leg Raise, Leg Up with Toes |

## Design Features

- **Okabe-Ito Palette**: Colorblind-safe colors
- **Large Typography**: 24pt steps, 22pt headings for low vision
- **Shape + Number ID**: ★1, ●2, ■3, ▲4 for cognitive accessibility
- **Goal Tracking Box**: Top-right corner for daily checkmarks
- **Laminate-Friendly**: Works with whiteboard markers on laminated sheets

## Installation

### Requirements
- Python 3.7+
- ReportLab 4.0+

```bash
pip install -r requirements.txt
```

## Documentation

- [Deployment Guide](docs/DEPLOYMENT.md)
- [Design System](docs/DESIGN.md)
- [API Reference](docs/API.md)

## Patient Use Cases

- Elderly patients (65+) with cognitive/vision impairment
- Post-stroke rehabilitation
- Physical therapy compliance tracking
- Home care coordination
- Care facility group sessions

## Contributing

Pull requests welcome. For major changes, open an issue first.

## License

MIT License - see LICENSE file

## Author

Created for P&L Dwyer Engineering + Australian Bitcoin Industry Body (ABIB)

---

## Roadmap

- [ ] Custom exercise library editor
- [ ] Patient progress tracking
- [ ] Mobile app version
- [ ] Multi-language support
- [ ] Ability-level variants (5s/10s/15s hold times)
- [ ] Integration with healthcare EMR systems
```

---

## Alternative: Use GitHub CLI (Faster)

```bash
# Install: https://cli.github.com

cd exerciseflow

# Create repo & push in one command
gh repo create exerciseflow --public --source=. --remote=origin --push
```

---

## GitHub Pages Deployment (Free Hosting)

```bash
# Enable GitHub Pages
# Settings → Pages → Source: main branch /root

# Your web interface will be live at:
# https://username.github.io/exerciseflow/web/caregiver-app.html
```

---

## GitHub Actions (Optional - Auto Tests)

Create `.github/workflows/test.yml`:

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/
```

---

## One-Liner Push (After Initial Setup)

```bash
git add . && git commit -m "Update: $(date +%Y-%m-%d)" && git push
```
