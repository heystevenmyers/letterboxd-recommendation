# Vercel Deployment Guide

This guide will help you deploy the frontend to Vercel and connect it to your backend API.

## 🎯 Overview

- **Frontend**: Deployed to Vercel (static hosting)
- **Backend**: Can be deployed separately (Railway, Render, Heroku, etc.) or run locally
- **Design**: Use Figma to design, then implement the styles in `styles.css`

## 📋 Prerequisites

1. A [Vercel account](https://vercel.com) (free tier works great!)
2. Git repository (GitHub, GitLab, or Bitbucket)
3. Backend API deployed somewhere (or running locally for testing)

## 🚀 Step 1: Prepare Your Frontend

The frontend is already configured for Vercel! The structure is:

```
frontend/
├── index.html          # Main page
├── app.js              # JavaScript (uses environment variables)
├── styles.css          # Styles (update with Figma designs)
├── vercel.json         # Vercel configuration
└── package.json        # Project metadata
```

## 🎨 Step 2: Design in Figma (Optional)

1. **Create your design** in Figma
2. **Export assets** (images, icons) if needed
3. **Get CSS values**:
   - Colors: Use the color picker in Figma, copy hex codes
   - Spacing: Use Figma's spacing measurements
   - Typography: Copy font families and sizes
   - Shadows/Borders: Copy border radius, shadow values

4. **Update `styles.css`** with your Figma design values

### Figma to CSS Tips:

```css
/* Example: Converting Figma values to CSS */

/* Figma: Color #667EEA */
background-color: #667EEA;

/* Figma: Spacing 24px */
padding: 24px;

/* Figma: Border radius 16px */
border-radius: 16px;

/* Figma: Shadow (X: 0, Y: 10, Blur: 30, Color: rgba(0,0,0,0.2)) */
box-shadow: 0 10px 30px rgba(0,0,0,0.2);
```

## 🌐 Step 3: Deploy to Vercel

### Option A: Deploy via Vercel Dashboard

1. **Push your code to GitHub/GitLab/Bitbucket**

2. **Go to [vercel.com](https://vercel.com)** and sign in

3. **Click "Add New Project"**

4. **Import your repository**

5. **Configure the project**:
   - **Root Directory**: Set to `frontend` (if your repo has both frontend and backend)
   - **Framework Preset**: Other (or leave blank for static site)
   - **Build Command**: Leave empty (no build needed)
   - **Output Directory**: `.` (current directory)

6. **Add Environment Variables**:
   - Click "Environment Variables"
   - Add: `API_URL` = `https://your-backend-api.com/api/analyze`
     - Replace with your actual backend URL

7. **Click "Deploy"**

### Option B: Deploy via CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend directory
cd frontend

# Deploy
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No (first time)
# - Project name? letterboxd-matcher (or your choice)
# - Directory? ./
# - Override settings? No

# Set environment variable
vercel env add API_URL
# Enter your backend URL when prompted

# Deploy to production
vercel --prod
```

## ⚙️ Step 4: Configure API URL

The frontend needs to know where your backend API is. You have two options:

### Option A: Environment Variable (Recommended)

1. In Vercel dashboard, go to your project
2. Settings → Environment Variables
3. Add:
   - **Name**: `API_URL`
   - **Value**: `https://your-backend-api.com/api/analyze`
   - **Environment**: Production, Preview, Development (select all)

4. Update `index.html` to use the environment variable:
   ```html
   <meta name="api-url" content="{{API_URL}}">
   ```

   Note: For static sites, you'll need to use Vercel's build-time replacement or a different approach.

### Option B: Update HTML Meta Tag Directly

Edit `frontend/index.html`:

```html
<meta name="api-url" content="https://your-backend-api.com/api/analyze">
```

Then commit and push - Vercel will redeploy automatically.

## 🔧 Step 5: Update app.js for Production

The `app.js` file already supports environment variables. It will:
1. Check for `window.API_URL` (injected by build script)
2. Check for meta tag `api-url`
3. Fall back to `http://localhost:5000` for local development

## 🎨 Step 6: Implement Figma Designs

1. **Open your Figma design**
2. **Inspect elements** to get:
   - Colors (hex codes)
   - Spacing (px values)
   - Typography (font, size, weight)
   - Borders (radius, width, color)
   - Shadows (offset, blur, color)

3. **Update `styles.css`** with these values

4. **Test locally**:
   ```bash
   cd frontend
   python -m http.server 3000
   # Open http://localhost:3000
   ```

5. **Commit and push** - Vercel will auto-deploy

## 🔗 Step 7: Deploy Backend (Optional)

Your backend can be deployed separately:

### Option A: Railway
```bash
# Install Railway CLI
npm i -g @railway/cli

# Deploy
railway login
railway init
railway up
```

### Option B: Render
1. Go to render.com
2. New → Web Service
3. Connect your repo
4. Set root directory to `backend`
5. Build command: `pip install -r requirements.txt`
6. Start command: `python app.py`

### Option C: Keep Local
- Run backend locally: `cd backend && python app.py`
- Update Vercel `API_URL` to `http://localhost:5000` (only works for local testing)

## ✅ Step 8: Test Your Deployment

1. Visit your Vercel URL (e.g., `https://your-app.vercel.app`)
2. Enter Letterboxd usernames
3. Check browser console (F12) for any errors
4. Verify API calls are going to the correct backend URL

## 🐛 Troubleshooting

### CORS Errors
If you see CORS errors, make sure your backend has CORS enabled:
```python
# In backend/app.py
from flask_cors import CORS
CORS(app)  # This should already be there
```

### API URL Not Working
- Check Vercel environment variables are set correctly
- Verify the meta tag in `index.html` has the correct URL
- Check browser console for the actual API URL being used

### Styles Not Updating
- Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)
- Check Vercel deployment logs
- Verify `styles.css` was committed and pushed

### Build Fails
- Make sure `vercel.json` is in the `frontend/` directory
- Check that all files are committed to git
- Review Vercel build logs for specific errors

## 📝 Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `API_URL` | Backend API endpoint | `https://api.example.com/api/analyze` |

## 🎓 Next Steps

1. **Custom Domain**: Add your own domain in Vercel settings
2. **Analytics**: Enable Vercel Analytics to track usage
3. **Performance**: Use Vercel's speed insights
4. **Design Updates**: Continue iterating on Figma and updating CSS

## 📚 Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Figma to CSS Guide](https://www.figma.com/community/plugin/1142246100403014947/css-to-figma)
- [Vercel Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)

