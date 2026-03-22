# GitHub Setup Guide — Stroke Recovery Program Cards

## Quick Start (5 minutes)

### 1. Create Repository on GitHub
```bash
# Go to github.com/new
# Repository name: SRP-Cards---Stroke-Recovery-Program-Cards
# Description: Personalized stroke recovery exercise cards for patients and caregivers
# Public/Private: Your choice
# Initialize with: README (NO - we'll create our own)
```

### 2. Clone & Setup Locally
```bash
# Create local directory
mkdir srp-cards && cd srp-cards

# Initialize git
git init
git config user.name "Your Name"
git config user.email "your@email.com"

# Add remote (replace USERNAME)
git remote add origin https://github.com/USERNAME/SRP-Cards---Stroke-Recovery-Program-Cards.git
git branch -M main
```

### 3. Project Structure
```
srp-cards/
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
│   ├── GITHUB_SETUP.md
│   └── QUICK_PUSH.md
└── examples/
```

### 4. Copy Files
```bash
cp exercise-sheet cli/
cp caregiver-app.html web/
cp system.html web/
cp index.html web/
chmod +x cli/exercise-sheet
```

### 5. Push to GitHub
```bash
git add .
git commit -m "Initial commit: Stroke Recovery Program Cards"
git push -u origin main
```

---

## Alternative: Use GitHub CLI (Faster)

```bash
# Install: https://cli.github.com

cd srp-cards

# Create repo & push in one command
gh repo create SRP-Cards---Stroke-Recovery-Program-Cards --public --source=. --remote=origin --push
```

---

## GitHub Pages Deployment (Free Hosting)

```bash
# Enable GitHub Pages
# Settings > Pages > Source: main branch /root

# Your caregiver interface will be live at:
# https://username.github.io/SRP-Cards---Stroke-Recovery-Program-Cards/web/caregiver-app.html
```

---

## GitHub Actions (Optional — Auto Tests)

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
