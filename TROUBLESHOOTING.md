# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### 1. CORS Error
**Error:** `Access to fetch at 'http://localhost:5000/api/analyze' from origin 'http://127.0.0.1:5000' has been blocked by CORS policy`

**Solution:**
- Make sure you're accessing the app via the same URL (either both `localhost` or both `127.0.0.1`)
- Hard refresh browser: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)
- Restart the Flask server after code changes

### 2. NoneType Comparison Error
**Error:** `'>=' not supported between instances of 'NoneType' and 'float'`

**Solution:**
- This should be fixed in the latest code
- **Restart your Flask server** - Python code changes require a restart
- Make sure you're running the updated `recommender.py`

### 3. Server Not Running
**Error:** `Failed to fetch` or `Connection refused`

**Solution:**
```bash
# Make sure venv is activated
source venv/bin/activate

# Start server
cd backend
python app.py
```

### 4. No Results Showing
**Possible causes:**
- User doesn't have any movies rated 3.5+ stars
- User profile is private
- Username is incorrect (case-sensitive)
- Scraping is still in progress (can take 30-60 seconds)

**Check:**
- Look at the terminal where Flask is running - you should see progress messages
- Check browser console for errors
- Try a different Letterboxd username

### 5. "User not found" Error
**Solution:**
- Verify the username is correct (Letterboxd usernames are case-sensitive)
- Make sure the profile is public (private profiles can't be scraped)
- Check the username on letterboxd.com first

### 6. JavaScript Not Loading
**Error:** `app.js:1 Failed to load resource`

**Solution:**
- Hard refresh browser to clear cache
- Check that `app.js` exists in `frontend/` directory
- Check browser console for 404 errors

### 7. Flask Server Crashes
**Check terminal for:**
- Import errors (missing packages)
- Syntax errors in Python files
- Port already in use (change port in `app.py`)

## Quick Diagnostic Steps

1. **Check server is running:**
   ```bash
   # Should see: "Running on http://127.0.0.1:5000"
   ```

2. **Check browser console (F12):**
   - Look for red error messages
   - Check Network tab to see if requests are being made

3. **Check Flask terminal:**
   - Should see: "Fetching movies for [username]..."
   - Look for any Python error messages

4. **Verify files are updated:**
   - Make sure you saved all file changes
   - Restart server after code changes

## Still Not Working?

Share:
1. The exact error message (copy/paste)
2. What you see in the browser console (F12)
3. What you see in the Flask terminal
4. What happens when you click "Find Matches"

