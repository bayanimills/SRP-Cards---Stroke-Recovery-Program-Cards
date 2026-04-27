# Recovery Program Cards — Quick Push Guide

## Step 1: Create Repo on GitHub (1 min)

1. Go to **github.com/new**
2. Name: `SRP-Cards---Stroke-Recovery-Program-Cards`
3. Description: `Personalized movement-practice exercise cards for individuals and facilitators`
4. Visibility: **Public** (or Private)
5. Create repository (don't initialize with README)

---

## Step 2: Setup Local Git (2 min)

```bash
cd srp-cards

git init
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Add GitHub as remote (REPLACE USERNAME)
git remote add origin https://github.com/USERNAME/SRP-Cards---Stroke-Recovery-Program-Cards.git
git branch -M main
```

---

## Step 3: Organize Files (1 min)

```bash
mkdir -p cli web docs examples

mv exercise-sheet cli/
mv index.html web/
mv system.html web/
mv index.html web/

chmod +x cli/exercise-sheet
```

---

## Step 4: Push to GitHub (1 min)

```bash
git add .

git commit -m "Initial commit: Recovery Program Cards

- CLI tool for PDF generation (exercise-sheet)
- Facilitator web interface (index.html)
- Admin documentation (system.html)
- Developer tool (index.html)
- Setup guides and documentation"

git push -u origin main
```

---

## Done!

Your repo is now live at: **github.com/USERNAME/SRP-Cards---Stroke-Recovery-Program-Cards**

---

## Next Steps (Optional)

### Enable GitHub Pages (Free Hosting)

```bash
# Go to Settings > Pages > Source: main branch
# Your app will be live at:
# https://USERNAME.github.io/SRP-Cards---Stroke-Recovery-Program-Cards/web/index.html
```

### Sync Changes

```bash
git add .
git commit -m "Description of changes"
git push
```

---

## Troubleshooting

### "fatal: not a git repository"
```bash
cd srp-cards
git status
```

### "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/USERNAME/SRP-Cards---Stroke-Recovery-Program-Cards.git
```

### Authentication Error
```bash
# Use GitHub CLI
gh auth login
git push
```

---

**Questions?** Check GITHUB_SETUP.md for detailed instructions.
