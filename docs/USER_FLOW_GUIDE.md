# User Flow & Information Flow Guide

## 🎬 Part 1: How a User Operates the App

### Step-by-Step User Experience

1. **User Opens the App**
   - Opens browser to `http://localhost:5000`
   - Sees a beautiful mobile-friendly interface with a form

2. **User Enters Username(s)**
   - Types their Letterboxd username in the first field (required)
   - Optionally types a second username to compare
   - Clicks "Find Matches" button

3. **Loading State**
   - Button changes to "Analyzing..."
   - Spinning loader appears
   - User sees "Analyzing your movie tastes..." message
   - **This can take 30-60 seconds** (scraping takes time!)

4. **Results Appear**
   - Page smoothly transitions to show results
   - Three main sections:
     - **Stats Card**: Shows total movies for each user and common movies
     - **Both Enjoyed**: Movies they both loved
     - **Recommendations**: Movies one person loved that the other should watch

5. **User Explores Results**
   - Scrolls through recommendations
   - Can click "View on Letterboxd →" links to see full movie pages
   - Can try different usernames to compare

---

## 🔄 Part 2: How Information Flows (Technical Deep Dive)

Let's trace a single request from button click to results display:

### **Phase 1: User Interaction (Frontend)**

```
User clicks "Find Matches" button
    ↓
JavaScript event listener catches the click
    ↓
Prevents default form submission (stops page refresh)
    ↓
Extracts usernames from form fields
    ↓
Shows loading spinner
    ↓
Prepares HTTP POST request
```

**Code Location**: `app.js` lines 20-40

```javascript
form.addEventListener('submit', async (e) => {
    e.preventDefault(); // Stop page refresh
    
    const user1 = document.getElementById('user1').value.trim();
    const user2 = document.getElementById('user2').value.trim();
    
    showLoading(); // Show spinner
    
    // Prepare to send request...
```

---

### **Phase 2: HTTP Request (Network)**

```
JavaScript creates POST request
    ↓
Request includes:
  - URL: http://localhost:5000/api/analyze
  - Method: POST
  - Headers: Content-Type: application/json
  - Body: { "user1": "stevenmyers", "user2": "friendname" }
    ↓
Request travels over network (localhost = same computer)
    ↓
Flask server receives request
```

**Code Location**: `app.js` lines 42-50

```javascript
const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        user1: user1,
        user2: user2 || null
    })
});
```

**Key Concept**: `fetch()` is asynchronous - JavaScript doesn't wait, it continues and comes back when response arrives.

---

### **Phase 3: Backend Processing (Flask Server)**

```
Flask receives POST request at /api/analyze route
    ↓
Extracts JSON data from request body
    ↓
Validates that at least user1 exists
    ↓
Calls scraper function: get_user_movies(user1)
```

**Code Location**: `app.py` lines 30-33

```python
@app.route('/api/analyze', methods=['POST'])
def analyze_users():
    data = request.json  # Extract JSON from request
    user1 = data.get('user1')
    user2 = data.get('user2')
    
    user1_movies = get_user_movies(user1)  # Start scraping
```

---

### **Phase 4: Web Scraping (Data Collection)**

This is where the magic happens! The scraper fetches data from Letterboxd:

```
get_user_movies("stevenmyers") is called
    ↓
Loop starts: page = 1
    ↓
Constructs URL: https://letterboxd.com/stevenmyers/films/page/1/
    ↓
Makes HTTP GET request to Letterboxd
    ↓
Receives HTML page (like what you see in browser)
    ↓
BeautifulSoup parses the HTML
    ↓
Finds all movie elements (<li class="poster-container">)
    ↓
For each movie:
  - Extracts title from <img alt="...">
  - Extracts rating from <span class="rated-4">
  - Extracts year from title or data attributes
  - Extracts URL from <a href="...">
    ↓
Stores in dictionary: { "Movie Title": {rating: 4, year: 2023, url: "..."} }
    ↓
Moves to next page (page = 2)
    ↓
Repeats until no more movies found
    ↓
Returns complete dictionary of all movies
```

**Code Location**: `letterboxd_scraper.py` lines 13-108

**Key Details**:
- **Pagination**: Letterboxd shows ~72 movies per page, so we loop through pages
- **Rate Limiting**: `time.sleep(1)` waits 1 second between requests (being polite!)
- **Error Handling**: If user doesn't exist or page fails, we catch and return error

**Example of what gets extracted**:
```python
{
    "The Matrix": {
        "rating": 4.5,
        "year": 1999,
        "url": "https://letterboxd.com/film/the-matrix/"
    },
    "Inception": {
        "rating": 5.0,
        "year": 2010,
        "url": "https://letterboxd.com/film/inception/"
    }
    # ... hundreds more movies
}
```

---

### **Phase 5: Recommendation Generation (Analysis)**

If two users provided, we compare their data:

```
get_user_movies(user1) returns: { "Movie A": {...}, "Movie B": {...} }
get_user_movies(user2) returns: { "Movie B": {...}, "Movie C": {...} }
    ↓
generate_recommendations() is called with both dictionaries
    ↓
Converts to sets for comparison:
  user1_titles = {"Movie A", "Movie B"}
  user2_titles = {"Movie B", "Movie C"}
    ↓
Finds intersection (both watched):
  both_watched = {"Movie B"}
    ↓
Filters for high ratings (4+ stars):
  both_enjoyed = [movies where both rated 4+]
    ↓
Finds user1's top movies user2 hasn't seen:
  user1_recommends = [movies user1 rated 4.5+ that user2 hasn't seen]
    ↓
Finds user2's top movies user1 hasn't seen:
  user2_recommends = [movies user2 rated 4.5+ that user1 hasn't seen]
    ↓
Sorts by rating (best first)
    ↓
Returns structured recommendations dictionary
```

**Code Location**: `recommender.py` lines 13-95

**Key Operations**:
- **Set Intersection** (`&`): Finds common elements
- **Set Difference**: Finds what one has that other doesn't
- **Filtering**: Only includes highly-rated movies
- **Sorting**: Orders by rating (best recommendations first)

**Example Output**:
```python
{
    "both_enjoyed": [
        {
            "title": "The Matrix",
            "user1_rating": 4.5,
            "user2_rating": 5.0,
            "year": 1999,
            "url": "..."
        }
    ],
    "user1_recommends": [
        {
            "title": "Inception",
            "rating": 5.0,
            "year": 2010,
            "url": "..."
        }
    ],
    "user2_recommends": [...],
    "stats": {
        "user1_total": 150,
        "user2_total": 200,
        "common_movies": 45
    }
}
```

---

### **Phase 6: Response Back to Frontend**

```
Flask converts Python dictionary to JSON
    ↓
Sends HTTP response:
  - Status: 200 (success)
  - Headers: Content-Type: application/json
  - Body: JSON string of recommendations
    ↓
Response travels back over network
    ↓
JavaScript receives response
```

**Code Location**: `app.py` line 50

```python
return jsonify(recommendations)  # Converts dict to JSON
```

---

### **Phase 7: Frontend Updates (Display Results)**

```
JavaScript receives JSON response
    ↓
Parses JSON back into JavaScript object
    ↓
Calls displayResults() function
    ↓
Updates DOM (Document Object Model):
  1. Updates stats numbers
  2. Creates movie cards for "both enjoyed"
  3. Creates movie cards for user1 recommendations
  4. Creates movie cards for user2 recommendations
    ↓
Hides loading spinner
    ↓
Shows results section with smooth animation
    ↓
User sees beautiful, organized recommendations!
```

**Code Location**: `app.js` lines 70-120

**Key Operations**:
- **DOM Manipulation**: Creating HTML elements dynamically
- **Template Strings**: Building HTML with movie data
- **Event Handling**: Making links clickable
- **CSS Classes**: Showing/hiding sections

**Example of creating a movie card**:
```javascript
const movieDiv = document.createElement('div');
movieDiv.className = 'movie-item';
movieDiv.innerHTML = `
    <div class="movie-title">The Matrix</div>
    <div class="movie-meta">
        <span class="movie-year">1999</span>
        <span class="movie-rating">⭐ 4.5/5</span>
        <a href="..." class="movie-link">View on Letterboxd →</a>
    </div>
`;
container.appendChild(movieDiv);
```

---

## 📊 Complete Flow Diagram

```
┌─────────────┐
│   USER      │
│  (Browser)  │
└──────┬──────┘
       │ 1. Enters usernames, clicks button
       ↓
┌─────────────────────────────────┐
│  FRONTEND (app.js)              │
│  - Validates input              │
│  - Shows loading spinner        │
│  - Creates POST request         │
└──────┬──────────────────────────┘
       │ 2. HTTP POST to /api/analyze
       ↓
┌─────────────────────────────────┐
│  BACKEND (app.py)               │
│  - Receives request             │
│  - Extracts usernames           │
└──────┬──────────────────────────┘
       │ 3. Calls scraper
       ↓
┌─────────────────────────────────┐
│  SCRAPER (letterboxd_scraper.py)│
│  - Loops through Letterboxd pages│
│  - Extracts movie data          │
│  - Returns dictionary           │
└──────┬──────────────────────────┘
       │ 4. Returns movie data
       ↓
┌─────────────────────────────────┐
│  RECOMMENDER (recommender.py)   │
│  - Compares user data           │
│  - Generates recommendations    │
│  - Returns structured results   │
└──────┬──────────────────────────┘
       │ 5. Returns recommendations
       ↓
┌─────────────────────────────────┐
│  BACKEND (app.py)                │
│  - Converts to JSON             │
│  - Sends HTTP response          │
└──────┬──────────────────────────┘
       │ 6. JSON response
       ↓
┌─────────────────────────────────┐
│  FRONTEND (app.js)               │
│  - Parses JSON                  │
│  - Updates DOM                  │
│  - Displays results             │
└──────┬──────────────────────────┘
       │ 7. User sees results
       ↓
┌─────────────┐
│   USER      │
│  (Browser)  │
└─────────────┘
```

---

## 🎯 Key Concepts Explained

### **1. Asynchronous Operations**
- Scraping takes 30-60 seconds
- JavaScript doesn't freeze - it uses `async/await`
- User sees loading spinner while waiting
- When done, results appear smoothly

### **2. Data Transformation**
```
HTML (Letterboxd) 
  → Python Dictionary (scraper)
    → Python Dictionary (recommender)
      → JSON (network)
        → JavaScript Object (frontend)
          → HTML (display)
```

### **3. Error Handling**
- If user doesn't exist → Error message shown
- If network fails → Error message shown
- If scraping fails → Error message shown
- User can always try again

### **4. State Management**
The app has different "states":
- **Initial**: Form visible, results hidden
- **Loading**: Spinner visible, form disabled
- **Results**: Results visible, form still accessible
- **Error**: Error message visible, can retry

---

## 🧪 Try It Yourself!

1. **Open browser DevTools** (F12)
2. **Go to Network tab** - you'll see the POST request
3. **Go to Console tab** - you'll see any errors
4. **Watch the flow**:
   - Click button → see request sent
   - Wait → see response received
   - See → page updates with results

This walkthrough shows exactly how modern web apps work - data flows from user input, through the backend, to external services, back through processing, and finally displayed to the user!

