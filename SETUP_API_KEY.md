# Setting Up Anthropic API Key

## Step 1: Get Your API Key

1. Go to https://console.anthropic.com/
2. Sign in or create an account
3. Navigate to **API Keys** in the dashboard
4. Click **Create Key**
5. Give it a name (e.g., "Letterboxd App")
6. Copy the API key (it starts with `sk-ant-...`)

## Step 2: Create .env File

1. In the project root directory, create a file named `.env`
2. Add the following line (replace with your actual API key):

```
ANTHROPIC_API_KEY=sk-ant-your-actual-api-key-here
```

**Important**: The `.env` file is already in `.gitignore`, so it won't be committed to git.

## Step 3: Install Dependencies

Make sure you have the latest dependencies installed:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Step 4: Test It

1. Start your Flask server:
   ```bash
   cd backend
   python app.py
   ```

2. Test with two users who have at least 3 movies both rated 4.5+ stars
3. The "Movies You'd Both Enjoy" section should show AI-generated recommendations

## For Production Deployment

When deploying to production (Vercel, Heroku, etc.):

1. **Never commit your `.env` file to git** (already in `.gitignore`)
2. Set the `ANTHROPIC_API_KEY` environment variable in your hosting platform's dashboard
3. The code will automatically load it from the environment

### Example for Vercel:
- Go to your project settings
- Navigate to Environment Variables
- Add: `ANTHROPIC_API_KEY` = `your-api-key-here`

### Example for Heroku:
```bash
heroku config:set ANTHROPIC_API_KEY=your-api-key-here
```

## Security Notes

✅ **Good**: API key is stored in `.env` file (not in code)  
✅ **Good**: `.env` is in `.gitignore` (won't be committed)  
✅ **Good**: API calls happen on backend only (key never exposed to browser)  
✅ **Good**: Environment variables used in production

## Troubleshooting

- **"ANTHROPIC_API_KEY not set"**: Make sure your `.env` file exists in the project root and has the correct key
- **"Invalid API key"**: Double-check you copied the entire key (they're long!)
- **No recommendations showing**: Make sure both users have at least 3 movies rated 4.5+ stars in common

