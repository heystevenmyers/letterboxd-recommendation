# Vercel Deployment Setup

This project has been configured for deployment on Vercel according to the [Vercel Flask documentation](https://vercel.com/docs/frameworks/backend/flask#exporting-the-flask-application).

## ✅ Changes Made for Vercel Compatibility

### 1. Entry Point (`app.py` at root)
- Created root-level `app.py` that imports from `backend/app.py`
- Vercel automatically detects this as the Flask application entrypoint

### 2. Static Files (`public/` directory)
- Moved all frontend files to `public/` directory
- Vercel automatically serves files from `public/**` via CDN
- Flask no longer uses `static_folder` on Vercel (only for local dev)

### 3. Flask App Configuration
- Updated `backend/app.py` to detect Vercel environment
- On Vercel: Static files served automatically, Flask handles API routes
- Local dev: Flask serves static files from `public/` directory

### 4. Vercel Configuration (`vercel.json`)
- Created root-level `vercel.json` for Flask deployment
- Configured security headers
- API routes are handled by Flask automatically

### 5. Dependencies
- Updated `requirements.txt` to use `anthropic>=0.74.0` (latest version)

## 📁 Project Structure

```
letterboxd-rec/
├── app.py                 # Vercel entry point (imports backend/app.py)
├── vercel.json            # Vercel configuration
├── requirements.txt       # Python dependencies
├── .vercelignore         # Files to exclude from deployment
├── public/                # Static files (served by Vercel CDN)
│   ├── index.html
│   ├── app.js
│   ├── styles.css
│   └── ...
└── backend/               # Flask application
    ├── app.py            # Main Flask app
    ├── ai_recommender.py
    ├── recommender.py
    └── letterboxd_scraper.py
```

## 🚀 Deployment Steps

1. **Push to Git Repository**
   ```bash
   git add .
   git commit -m "Configure for Vercel deployment"
   git push
   ```

2. **Deploy to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Import your Git repository
   - Vercel will auto-detect Flask framework
   - No build command needed (set to `null` in vercel.json)

3. **Set Environment Variables**
   In Vercel dashboard → Settings → Environment Variables:
   - `ANTHROPIC_API_KEY`: Your Anthropic API key (starts with `sk-ant-`)
   - Add to: Production, Preview, and Development environments

4. **Deploy**
   - Click "Deploy"
   - Vercel will install dependencies and deploy your Flask app

## 🔍 How It Works on Vercel

1. **Static Files**: Files in `public/` are served directly by Vercel's CDN
   - `/` → `public/index.html`
   - `/styles.css` → `public/styles.css`
   - `/app.js` → `public/app.js`

2. **API Routes**: Handled by Flask (Vercel Function)
   - `/api/analyze` → Flask route
   - `/api/health` → Flask route
   - All other non-static routes → Flask (404 if not defined)

3. **Environment Detection**:
   - Vercel sets `VERCEL=1` environment variable
   - Flask app detects this and disables static file serving
   - Static files are served by Vercel CDN instead

## 🧪 Local Development

To test locally:

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Flask app
python app.py
# or
cd backend && python app.py
```

The app will serve static files from `public/` directory when running locally.

## ⚠️ Important Notes

1. **Environment Variables**: Make sure to set `ANTHROPIC_API_KEY` in Vercel dashboard
2. **Static Files**: Don't modify files in `frontend/` - use `public/` instead
3. **API Routes**: All API routes must start with `/api/` to avoid conflicts with static files
4. **File Size**: Total deployment must be under 250MB (Vercel Functions limit)

## 📚 References

- [Vercel Flask Documentation](https://vercel.com/docs/frameworks/backend/flask#exporting-the-flask-application)
- [Vercel Functions Limits](https://vercel.com/docs/functions/runtimes/python#limitations)

