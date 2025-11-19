# Learning Guide: How This App Works

## 🏗️ Architecture Overview

This app has two main parts:
1. **Frontend** (what users see): HTML, CSS, JavaScript
2. **Backend** (the server): Python with Flask

They communicate using **HTTP requests** (like when you visit a website).

---

## 📱 Frontend (Client-Side)

### HTML (`index.html`)
- **What it is**: The structure of your webpage
- **Key concepts**:
  - `<form>`: Collects user input (usernames)
  - `<section>`: Organizes content into sections
  - `id` attributes: Let JavaScript find and modify elements

### CSS (`styles.css`)
- **What it is**: Makes your page look good
- **Key concepts**:
  - **Mobile-first design**: We style for phones first, then add tablet/desktop styles
  - **Flexbox/Grid**: Modern ways to layout elements
  - **Responsive design**: The page adapts to different screen sizes

### JavaScript (`app.js`)
- **What it is**: Makes your page interactive
- **Key concepts**:
  - **Event listeners**: React to user actions (like clicking a button)
  - **fetch()**: Makes HTTP requests to your backend
  - **async/await**: Handles asynchronous operations (waiting for server responses)
  - **DOM manipulation**: Changes what's displayed on the page

**Flow:**
1. User enters usernames and clicks "Find Matches"
2. JavaScript prevents default form submission
3. Sends POST request to backend with usernames
4. Shows loading spinner
5. When response comes back, displays results

---

## 🖥️ Backend (Server-Side)

### Flask (`app.py`)
- **What it is**: A Python web framework (makes it easy to create web servers)
- **Key concepts**:
  - **Routes**: URLs that trigger functions (like `/api/analyze`)
  - **POST requests**: Used when sending data (like usernames)
  - **JSON**: Data format for sending/receiving structured data
  - **CORS**: Allows frontend to talk to backend from different origins

**Flow:**
1. Receives POST request with usernames
2. Calls scraper to get movie data
3. Calls recommender to generate suggestions
4. Returns JSON response with recommendations

### Web Scraping (`letterboxd_scraper.py`)
- **What it is**: Extracting data from websites
- **Key concepts**:
  - **HTTP requests**: Fetching web pages (like a browser does)
  - **HTML parsing**: Reading the structure of a webpage
  - **BeautifulSoup**: Library that makes parsing HTML easier
  - **Rate limiting**: Waiting between requests (being polite to servers)

**How it works:**
1. Constructs URL: `https://letterboxd.com/{username}/films/page/1/`
2. Fetches the HTML page
3. Parses HTML to find movie elements
4. Extracts: title, rating, year, URL
5. Loops through all pages (pagination)

### Recommendation Engine (`recommender.py`)
- **What it is**: Logic to suggest movies
- **Key concepts**:
  - **Set operations**: Finding common elements (`&`), differences (`-`)
  - **Filtering**: Only including movies with high ratings
  - **Sorting**: Ordering by rating (best first)

**Three types of recommendations:**
1. **Both enjoyed**: Movies in both lists with 4+ stars
2. **Cross-recommendations**: Movies one loved (4.5+) that the other hasn't seen
3. **New suggestions**: Movies neither has seen (currently empty - you can expand this!)

---

## 🔄 How Data Flows

```
User Input (HTML form)
    ↓
JavaScript (app.js)
    ↓
HTTP POST Request
    ↓
Flask Server (app.py)
    ↓
Scraper (letterboxd_scraper.py) → Fetches data from Letterboxd
    ↓
Recommender (recommender.py) → Analyzes and generates suggestions
    ↓
JSON Response
    ↓
JavaScript (app.js) → Updates the page
    ↓
User sees results!
```

---

## 🎓 Key Programming Concepts

### 1. **Asynchronous Programming**
- When you fetch data from a server, it takes time
- `async/await` lets your code wait without freezing the page
- Example: `const data = await fetch(url)`

### 2. **API Design**
- RESTful APIs use HTTP methods: GET (read), POST (create/send data)
- JSON is the standard format for data exchange
- Endpoints are like functions you can call over the internet

### 3. **Error Handling**
- Always wrap risky operations in try/catch
- Show user-friendly error messages
- Handle edge cases (empty results, network failures)

### 4. **State Management**
- Show/hide different sections based on app state
- Loading → Results → Error states
- Use CSS classes to toggle visibility

---

## 🚀 Next Steps to Learn

1. **Improve the scraper**: Handle more edge cases, extract genres/directors
2. **Better recommendations**: Use machine learning or external movie APIs
3. **Caching**: Store results so you don't re-scrape every time
4. **User accounts**: Let users save their comparisons
5. **Deployment**: Put it online (Heroku, Vercel, etc.)

---

## 🐛 Debugging Tips

1. **Browser DevTools**: Press F12 to see console errors and network requests
2. **Python print statements**: Add `print()` to see what's happening
3. **Check the Network tab**: See if requests are failing
4. **Test endpoints separately**: Use Postman or curl to test the API

---

## 📚 Resources

- **Flask**: https://flask.palletsprojects.com/
- **BeautifulSoup**: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- **JavaScript fetch**: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- **CSS Grid/Flexbox**: https://css-tricks.com/snippets/css/complete-guide-grid/

