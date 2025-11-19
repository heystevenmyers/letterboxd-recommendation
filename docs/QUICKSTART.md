# Quick Start Guide

## 🚀 Getting Started

### Step 1: Install Python Dependencies

Make sure you have Python 3.7+ installed, then run:

```bash
pip install -r requirements.txt
```

Or if you prefer using a virtual environment (recommended):

```bash
# Create virtual environment
python3 -m venv venv

# Activate it (Mac/Linux)
source venv/bin/activate

# Or on Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Start the Server

```bash
cd backend
python app.py
```

You should see:
```
Starting Letterboxd Recommendation Server...
Open http://localhost:5000 in your browser
 * Running on http://127.0.0.1:5000
```

**Note**: Make sure you're in the `backend/` directory when running the server, as it needs to import the other Python modules.

### Step 3: Open the App

1. Open your browser and go to: `http://localhost:5000`
2. You'll see the mobile-friendly interface
3. Enter one or two Letterboxd usernames
4. Click "Find Matches"

## 📱 Testing

Try with these public Letterboxd accounts (if they exist):
- Enter one username to see their movies
- Enter two usernames to see comparisons

## ⚠️ Important Notes

1. **Rate Limiting**: The scraper waits 1 second between requests to be polite to Letterboxd's servers
2. **Privacy**: Only works with public Letterboxd profiles
3. **Performance**: Scraping can take 30-60 seconds per user (depending on how many movies they've watched)

## 🐛 Troubleshooting

### "Connection refused" error
- Make sure the Flask server is running (`cd backend && python app.py`)
- Check that port 5000 isn't being used by another app
- Make sure you're running from the `backend/` directory

### "User not found" error
- Make sure the username is correct (case-sensitive)
- The profile must be public

### No movies showing up
- The user might not have rated movies 3.5+ stars
- Try a different username with more ratings

### Slow loading
- This is normal! Scraping takes time
- Each user might have hundreds of movies across multiple pages

## 🎓 Next Steps

1. Read `docs/LEARNING_GUIDE.md` to understand how everything works
2. Try modifying the code to see what happens
3. Add new features (genres, directors, better recommendations)

