# Frontend - Letterboxd Movie Matcher

This is the frontend for the Letterboxd Movie Matcher app, designed to be deployed on Vercel.

## 🚀 Quick Start (Local Development)

```bash
# Serve locally
python -m http.server 3000

# Or use any static server
npx serve .
```

Open `http://localhost:3000` in your browser.

## 📁 File Structure

```
frontend/
├── index.html          # Main HTML page
├── app.js              # JavaScript logic
├── styles.css          # All styles (update with Figma designs)
├── vercel.json         # Vercel deployment config
├── package.json        # Project metadata
└── README.md           # This file
```

## 🎨 Updating Styles from Figma

1. Open your Figma design
2. Select an element
3. Copy CSS values:
   - **Colors**: Right-click → Copy as CSS
   - **Spacing**: Check the spacing values in the right panel
   - **Typography**: Check font family, size, weight
   - **Shadows**: Check shadow properties
4. Update `styles.css` with these values

## 🌐 Deploying to Vercel

See [../docs/VERCEL_DEPLOYMENT.md](../docs/VERCEL_DEPLOYMENT.md) for detailed instructions.

Quick version:
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel

# Set environment variable
vercel env add API_URL
# Enter: https://your-backend-api.com/api/analyze
```

## ⚙️ Configuration

### API URL

The frontend needs to know where your backend API is located. Set this via:

1. **Environment Variable** (Vercel): Set `API_URL` in Vercel dashboard
2. **Meta Tag** (HTML): Update the `<meta name="api-url">` tag in `index.html`
3. **Local Development**: Defaults to `http://localhost:5000/api/analyze`

## 🔧 Development

### Local Testing with Backend

1. Start backend: `cd ../backend && python app.py`
2. Start frontend: `python -m http.server 3000`
3. Open `http://localhost:3000`

### Updating Styles

Edit `styles.css` directly. The file uses:
- Mobile-first responsive design
- CSS Grid and Flexbox
- CSS custom properties (can be added for theming)

### Adding Features

- **New UI components**: Add HTML to `index.html`, styles to `styles.css`
- **New functionality**: Add JavaScript to `app.js`
- **API changes**: Update `API_URL` and fetch calls in `app.js`

## 📱 Mobile-First Design

The CSS is written mobile-first:
- Base styles target mobile devices
- `@media (min-width: 768px)` adds tablet/desktop styles
- All breakpoints are defined in `styles.css`

## 🎯 Figma Integration Tips

1. **Export Assets**: Use Figma's export feature for images/icons
2. **Copy CSS**: Use Figma plugins to copy CSS directly
3. **Measurements**: Use Figma's measurement tool for spacing
4. **Colors**: Use Figma's color picker to get exact hex codes
5. **Typography**: Match font families, sizes, and weights exactly

## 📚 Resources

- [Vercel Docs](https://vercel.com/docs)
- [Figma to Code](https://www.figma.com/community/plugin/1142246100403014947/css-to-figma)
- [MDN Web Docs](https://developer.mozilla.org/)

