# 🐍 Virtual Environment Setup (No Xcode Required)

## Option 1: Use virtualenv (Recommended - No Xcode Needed)

`virtualenv` is a standalone package that doesn't require Xcode tools.

### Step 1: Install virtualenv (if not already installed)

```bash
# Try installing with pip3 (might work without Xcode)
pip3 install --user virtualenv
```

If that doesn't work, try:
```bash
# Use easy_install (comes with Python)
easy_install --user virtualenv
```

### Step 2: Create Virtual Environment

```bash
cd "/Users/stevenmyers/letterboxd project"

# Create venv using virtualenv
virtualenv venv
```

If `virtualenv` command is not found, use:
```bash
python3 -m virtualenv venv
```

### Step 3: Activate and Install

```bash
# Activate
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

---

## Option 2: Install Packages Globally (Simplest - No Virtual Environment)

If you just want to get running quickly without a virtual environment:

```bash
cd "/Users/stevenmyers/letterboxd project"

# Install packages to your user directory (doesn't require sudo)
pip3 install --user -r requirements.txt
```

Then run:
```bash
cd backend
python3 app.py
```

**Note:** This installs packages globally for your user, not in an isolated environment.

---

## Option 3: Use Homebrew Python (If You Have Homebrew)

If you have Homebrew installed:

```bash
# Install Python via Homebrew (includes venv)
brew install python3

# Then create venv normally
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Option 4: Use Anaconda/Miniconda (If Installed)

If you have Anaconda or Miniconda:

```bash
cd "/Users/stevenmyers/letterboxd project"

# Create conda environment
conda create -n letterboxd python=3.9
conda activate letterboxd

# Install packages
pip install -r requirements.txt
```

---

## ✅ Recommended: Try Option 1 First

The `virtualenv` package usually works without Xcode:

```bash
# One-time setup
pip3 install --user virtualenv
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

# Then run the app
cd backend
python app.py
```

---

## 🔍 Check What You Have

Run these to see what's available:

```bash
# Check Python
python3 --version

# Check if virtualenv is available
python3 -m virtualenv --version

# Check if pip works
pip3 --version
```

If any of these work, you can proceed without Xcode!

