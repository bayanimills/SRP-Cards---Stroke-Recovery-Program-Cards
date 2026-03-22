# 🚀 ExerciseFlow → GitHub in 5 Minutes

## Step 1: Create Repo on GitHub (1 min)

1. Go to **github.com/new**
2. Name: `exerciseflow`
3. Description: `Personalized rehabilitation exercise sheet generator`
4. Visibility: **Public** (or Private)
5. ✅ Create repository (don't initialize with README)

---

## Step 2: Setup Local Git (2 min)

```bash
# Navigate to outputs directory
cd /mnt/user-data/outputs

# Initialize git
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Add GitHub as remote (REPLACE USERNAME)
git remote add origin https://github.com/USERNAME/exerciseflow.git
git branch -M main
```

---

## Step 3: Organize Files (1 min)

```bash
# Create folder structure
mkdir -p cli web docs examples

# Move files into folders
mv exercise-sheet cli/
mv caregiver-app.html web/
mv system.html web/
mv index.html web/

# Make CLI executable
chmod +x cli/exercise-sheet

# Verify structure
tree  # or: ls -la cli/ web/ docs/
```

---

## Step 4: Add & Push to GitHub (1 min)

```bash
# Stage all files
git add .

# Create initial commit
git commit -m "Initial commit: ExerciseFlow rehabilitation exercise generator

- CLI tool for PDF generation (exercise-sheet)
- Web interface for caregivers (caregiver-app.html)
- Admin documentation (system.html)
- Developer tool (index.html)
- Complete README and setup guides"

# Push to GitHub
git push -u origin main
```

---

## Done! ✅

Your repo is now live at: **github.com/USERNAME/exerciseflow**

---

## Next Steps (Optional)

### Enable GitHub Pages (Free Hosting)

```bash
# Go to Settings → Pages → Source: main branch
# Then your web app is live at:
# https://USERNAME.github.io/exerciseflow/web/caregiver-app.html
```

### Set Up Local Development Server

```bash
# Python 3
python3 -m http.server 8000

# Then visit: http://localhost:8000/web/caregiver-app.html
```

### Sync Changes Back to GitHub

```bash
# After making changes locally:
git add .
git commit -m "Description of changes"
git push
```

---

## Troubleshooting

### "fatal: not a git repository"
```bash
# Make sure you're in the right directory
cd /mnt/user-data/outputs
git status
```

### "remote origin already exists"
```bash
# Remove old remote and add new one
git remote remove origin
git remote add origin https://github.com/USERNAME/exerciseflow.git
```

### Authentication Error
```bash
# Use GitHub CLI instead (easier)
brew install gh  # or apt-get install gh

# Then authenticate once
gh auth login

# And push
git push
```

---

## One-Line Setup (for brave users)

```bash
cd /mnt/user-data/outputs && \
git init && \
git config user.name "Your Name" && \
git config user.email "your.email@example.com" && \
git remote add origin https://github.com/USERNAME/exerciseflow.git && \
git add . && \
git commit -m "Initial commit: ExerciseFlow" && \
git branch -M main && \
git push -u origin main
```

Replace `USERNAME` with your GitHub username, then you're done.

---

**Questions?** Check the GITHUB_SETUP.md file for detailed instructions.