# 🐍 Setting Up Virtual Environment

## Step-by-Step Instructions

### Step 1: Navigate to Project Directory

```bash
cd "/Users/stevenmyers/letterboxd project"
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
```

This creates a folder called `venv` with a fresh Python environment.

**Note:** If you get an error about Xcode tools, you need to install them first:
```bash
xcode-select --install
```
Then wait for the installation to complete before continuing.

### Step 3: Activate the Virtual Environment

```bash
source venv/bin/activate
```

**You'll know it's activated when you see `(venv)` at the start of your terminal prompt:**
```
(venv) stevenmyers@Mac letterboxd project %
```

### Step 4: Upgrade pip (Optional but Recommended)

```bash
pip install --upgrade pip
```

### Step 5: Install All Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- flask-cors (CORS support)
- beautifulsoup4 (web scraping)
- requests (HTTP requests)
- lxml (HTML parsing)

### Step 6: Verify Installation

```bash
pip list
```

You should see all the packages listed.

## ✅ You're Done!

Now you can run the app:

```bash
# Make sure venv is activated (you should see (venv) in prompt)
source venv/bin/activate

# Go to backend directory
cd backend

# Start the server
python app.py
```

## 🔄 Using the Virtual Environment Later

Every time you open a new terminal and want to run the app:

1. **Navigate to project:**
   ```bash
   cd "/Users/stevenmyers/letterboxd project"
   ```

2. **Activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Run the app:**
   ```bash
   cd backend
   python app.py
   ```

## 🚪 Deactivating Virtual Environment

When you're done, you can deactivate:
```bash
deactivate
```

## ❓ Troubleshooting

### "python3: command not found"
Try:
```bash
python -m venv venv
```

### "No module named venv"
Your Python might not have venv. Try:
```bash
python3 -m virtualenv venv
pip install virtualenv
```

### "Permission denied"
Make sure you're not using sudo. Virtual environments should be created in your project directory without sudo.

### Packages not installing
Make sure the virtual environment is activated (you see `(venv)` in your prompt).

## 📝 Quick Reference

```bash
# Create venv (one time only)
python3 -m venv venv

# Activate venv (every time you work on the project)
source venv/bin/activate

# Install packages (one time, after creating venv)
pip install -r requirements.txt

# Run the app
cd backend
python app.py

# Deactivate venv (when done)
deactivate
```

