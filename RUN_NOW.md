# 🚀 How to Run Right Now

## Quick Start (3 Steps)

### Step 1: Create Virtual Environment & Install Dependencies

**Option A: Use the setup script (Recommended)**
```bash
# Make sure you're in the project root
cd "/Users/stevenmyers/letterboxd project"

# Run the setup script
chmod +x setup.sh
./setup.sh
```

**Option B: Manual setup**
```bash
# Make sure you're in the project root
cd "/Users/stevenmyers/letterboxd project"

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

**Note:** If you get an error about Xcode command line tools, install them first:
```bash
xcode-select --install
```

### Step 2: Activate Virtual Environment & Start Server

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Navigate to backend directory
cd backend

# Start the Flask server
python app.py
```

**Note:** You need to activate the virtual environment each time you open a new terminal:
```bash
source venv/bin/activate
```

You should see:
```
Starting Letterboxd Recommendation Server...
Open http://localhost:5000 in your browser
 * Running on http://127.0.0.1:5000
```

### Step 3: Open in Browser

Open your browser and go to:
```
http://localhost:5000
```

That's it! The app should be running.

## What You'll See

1. A form to enter Letterboxd usernames
2. Enter one or two usernames
3. Click "Find Matches"
4. Wait 30-60 seconds (scraping takes time)
5. See your movie recommendations!

## Troubleshooting

### "Command not found: python3"
Try:
```bash
python app.py
```
or
```bash
python3.9 app.py
```

### "Module not found" errors
Make sure you installed requirements:
```bash
pip3 install -r requirements.txt
```

### Port 5000 already in use
Change the port in `backend/app.py`:
```python
app.run(debug=True, port=5001)  # Change 5000 to 5001
```
Then open `http://localhost:5001`

### Can't connect to backend
- Make sure the Flask server is running
- Check the terminal for error messages
- Make sure you're opening `http://localhost:5000` (not 3000)

## Running Both Separately (Advanced)

If you want to run frontend and backend separately:

**Terminal 1 - Backend:**
```bash
cd backend
python3 app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
python3 -m http.server 3000
```

Then open `http://localhost:3000` and update the API URL in `frontend/index.html` to point to `http://localhost:5000/api/analyze`

