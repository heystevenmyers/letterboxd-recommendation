# 🎬 Letterboxd Movie Recommendation App

A mobile-first web app that compares two Letterboxd accounts and recommends movies based on shared preferences.

## ✨ Features

- **Compare two Letterboxd accounts** to find movie matches
- **Three types of recommendations**:
  - 🎯 Movies both watched and enjoyed (4+ stars)
  - ⭐ Movies one person loved that the other would enjoy
  - 🆕 Movies neither has seen (coming soon with genre analysis)
- **Mobile-optimized** responsive design
- **Real-time analysis** of Letterboxd profiles

## 🏗️ How It Works

1. **Data Collection**: Scrapes Letterboxd user profiles to get watched movies and ratings
2. **Analysis**: Compares two users' movie data using set operations and filtering
3. **Recommendations**: Generates personalized suggestions based on ratings and preferences

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3 (mobile-first), Vanilla JavaScript
  - **Deployment**: Vercel (static hosting)
  - **Design**: Figma-ready (easy to implement designs)
- **Backend**: Python 3.7+ with Flask
- **Scraping**: BeautifulSoup4 + Requests
- **No frameworks** - pure code for learning!

## 🚀 Quick Start

See [docs/QUICKSTART.md](docs/QUICKSTART.md) for detailed setup instructions.

**TL;DR:**
```bash
pip install -r requirements.txt
cd backend
python app.py
# Open http://localhost:5000
```

## 📚 Learning Resources

- **[docs/LEARNING_GUIDE.md](docs/LEARNING_GUIDE.md)**: Comprehensive explanation of how everything works
- **[docs/QUICKSTART.md](docs/QUICKSTART.md)**: Step-by-step setup guide
- **[docs/USER_FLOW_GUIDE.md](docs/USER_FLOW_GUIDE.md)**: How users interact with the app
- **[docs/CODE_WALKTHROUGH.md](docs/CODE_WALKTHROUGH.md)**: Detailed code execution trace with examples
- **[docs/VERCEL_DEPLOYMENT.md](docs/VERCEL_DEPLOYMENT.md)**: Deploy frontend to Vercel

## ⚠️ Important Notes

- Only works with **public** Letterboxd profiles
- Scraping respects rate limits (1 second between requests)
- May take 30-60 seconds per user depending on movie count
- This is a learning project - be respectful of Letterboxd's servers!

## 🎓 What You'll Learn

- Web scraping with BeautifulSoup
- Building REST APIs with Flask
- Frontend-backend communication
- Mobile-first responsive design
- JavaScript async/await
- Data analysis and recommendation algorithms

## 📝 Project Structure

```
letterboxd project/
├── backend/                    # Python backend code
│   ├── app.py                  # Flask server
│   ├── letterboxd_scraper.py   # Web scraping logic
│   └── recommender.py          # Recommendation algorithm
├── frontend/                   # Frontend web files
│   ├── index.html              # Main HTML page
│   ├── styles.css              # Mobile-first CSS
│   └── app.js                  # Frontend JavaScript
├── docs/                       # Documentation
│   ├── LEARNING_GUIDE.md       # How everything works
│   ├── QUICKSTART.md           # Setup instructions
│   ├── USER_FLOW_GUIDE.md      # User experience guide
│   └── CODE_WALKTHROUGH.md     # Code execution trace
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

