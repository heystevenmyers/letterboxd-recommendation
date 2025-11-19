# Code Walkthrough: Following a Real Request

Let's trace through what happens when a user enters "stevenmyers" and "friendname" and clicks "Find Matches".

---

## 🎬 Scene 1: User Clicks Button

**File**: `app.js`  
**Location**: Line 21

```javascript
form.addEventListener('submit', async (e) => {
    e.preventDefault(); // Stops the form from refreshing the page
```

**What happens**:
- User clicks "Find Matches"
- Browser would normally submit form and refresh page
- `e.preventDefault()` stops that behavior
- We handle it with JavaScript instead

**Current state**:
- `user1 = "stevenmyers"`
- `user2 = "friendname"`

---

## 🎬 Scene 2: Preparing the Request

**File**: `app.js`  
**Location**: Lines 33-49

```javascript
showLoading();  // Shows spinner, disables button
hideResults();  // Hides any previous results
hideError();    // Hides any previous errors

const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        user1: "stevenmyers",
        user2: "friendname"
    })
});
```

**What happens**:
1. UI updates: spinner appears, button says "Analyzing..."
2. JavaScript creates HTTP request
3. Converts JavaScript object to JSON string: `'{"user1":"stevenmyers","user2":"friendname"}'`
4. Sends POST request to `http://localhost:5000/api/analyze`
5. **`await`** means: "Wait here until response comes back (could be 60 seconds!)"

**Visual**: User sees spinner spinning, button disabled

---

## 🎬 Scene 3: Flask Receives Request

**File**: `app.py`  
**Location**: Lines 30-49

```python
@app.route('/api/analyze', methods=['POST'])
def analyze_users():
    data = request.json  # Extracts: {"user1": "stevenmyers", "user2": "friendname"}
    user1 = data.get('user1')  # "stevenmyers"
    user2 = data.get('user2')  # "friendname"
    
    print(f"Fetching movies for {user1}...")  # Console: "Fetching movies for stevenmyers..."
    user1_movies = get_user_movies(user1)  # This takes 30-60 seconds!
```

**What happens**:
- Flask's routing system matches `/api/analyze` to `analyze_users()` function
- `request.json` automatically parses JSON string back to Python dictionary
- Extracts usernames
- Calls scraper function (this is the slow part!)

**Visual**: Terminal/console shows: `"Fetching movies for stevenmyers..."`

---

## 🎬 Scene 4: Scraping User 1's Movies

**File**: `letterboxd_scraper.py`  
**Location**: Lines 13-108

```python
def get_user_movies(username):  # username = "stevenmyers"
    movies = {}
    page = 1
    
    while True:  # Loop through all pages
        url = f"https://letterboxd.com/stevenmyers/films/page/{page}/"
        # First iteration: page 1, then 2, then 3...
```

**What happens on Page 1**:

1. **HTTP Request**:
   ```python
   response = requests.get("https://letterboxd.com/stevenmyers/films/page/1/", headers={...})
   ```
   - Sends GET request to Letterboxd
   - Receives HTML page (thousands of lines of HTML)

2. **Parse HTML**:
   ```python
   soup = BeautifulSoup(response.content, 'lxml')
   movie_elements = soup.find_all('li', class_='poster-container')
   ```
   - BeautifulSoup reads the HTML
   - Finds all `<li class="poster-container">` elements (each is a movie)

3. **Extract Data for Each Movie**:
   ```python
   for element in movie_elements:  # Loop through ~72 movies per page
       img = element.find('img')
       title = img.get('alt', '').strip()  # "The Matrix (1999)"
       
       rating_elem = element.find('span', class_='rating')
       # Finds class like "rated-4" or "rated-4-half"
       rating = 4.5  # Extracted from CSS class
       
       movies[title] = {
           'rating': 4.5,
           'year': 1999,
           'url': 'https://letterboxd.com/film/the-matrix/'
       }
   ```

4. **After Page 1**:
   ```python
   movies = {
       "The Matrix (1999)": {"rating": 4.5, "year": 1999, "url": "..."},
       "Inception (2010)": {"rating": 5.0, "year": 2010, "url": "..."},
       # ... ~70 more movies
   }
   ```

5. **Move to Next Page**:
   ```python
   page += 1  # Now page = 2
   time.sleep(1)  # Wait 1 second (be polite!)
   # Loop continues...
   ```

6. **Eventually**:
   - Page 3 has no movies → `movie_elements` is empty
   - `break` exits the loop
   - Returns complete dictionary

**Final result for user1**:
```python
user1_movies = {
    "The Matrix": {"rating": 4.5, "year": 1999, "url": "..."},
    "Inception": {"rating": 5.0, "year": 2010, "url": "..."},
    "Parasite": {"rating": 4.5, "year": 2019, "url": "..."},
    # ... 150 total movies
}
```

**Time taken**: ~45 seconds (3 pages × 15 seconds per page)

---

## 🎬 Scene 5: Scraping User 2's Movies

**File**: `app.py`  
**Location**: Lines 51-53

```python
if user2:  # user2 = "friendname"
    print(f"Fetching movies for {user2}...")
    user2_movies = get_user_movies(user2)  # Another 30-60 seconds!
```

**Same process repeats** for the second user.

**Final result for user2**:
```python
user2_movies = {
    "The Matrix": {"rating": 5.0, "year": 1999, "url": "..."},
    "Blade Runner": {"rating": 4.5, "year": 1982, "url": "..."},
    "Dune": {"rating": 5.0, "year": 2021, "url": "..."},
    # ... 200 total movies
}
```

**Time taken**: Another ~50 seconds

**Total scraping time**: ~95 seconds (user sees spinner this whole time!)

---

## 🎬 Scene 6: Generating Recommendations

**File**: `app.py` → `recommender.py`  
**Location**: `recommender.py` lines 13-95

```python
def generate_recommendations(user1_movies, user2_movies):
    # Convert to sets for easy comparison
    user1_titles = set(user1_movies.keys())
    # {"The Matrix", "Inception", "Parasite", ...}
    
    user2_titles = set(user2_movies.keys())
    # {"The Matrix", "Blade Runner", "Dune", ...}
```

**Step 1: Find Movies Both Watched**:
```python
both_watched = user1_titles & user2_titles  # Set intersection
# Result: {"The Matrix", ...}  # Movies in BOTH sets
```

**Step 2: Filter for High Ratings**:
```python
both_enjoyed = []
for title in both_watched:  # "The Matrix"
    rating1 = user1_movies[title].get('rating', 0)  # 4.5
    rating2 = user2_movies[title].get('rating', 0)  # 5.0
    
    if rating1 >= 4.0 and rating2 >= 4.0:  # Both rated 4+ stars
        both_enjoyed.append({
            'title': "The Matrix",
            'user1_rating': 4.5,
            'user2_rating': 5.0,
            'year': 1999,
            'url': '...'
        })
```

**Step 3: Find User 1's Recommendations for User 2**:
```python
user1_recommends = []
for title, data in user1_movies.items():
    if title not in user2_titles:  # User 2 hasn't seen it
        if data.get('rating', 0) >= 4.5:  # User 1 loved it (4.5+)
            user1_recommends.append({
                'title': title,
                'rating': data.get('rating'),
                # ...
            })
# Result: ["Inception", "Parasite", ...]  # User 1's top picks
```

**Step 4: Find User 2's Recommendations for User 1**:
```python
# Same logic, but reversed
user2_recommends = [...]  # ["Blade Runner", "Dune", ...]
```

**Step 5: Sort and Limit**:
```python
user1_recommends.sort(key=lambda x: x['rating'], reverse=True)
user1_recommends = user1_recommends[:20]  # Top 20 only
```

**Final recommendations dictionary**:
```python
recommendations = {
    'both_enjoyed': [
        {'title': 'The Matrix', 'user1_rating': 4.5, 'user2_rating': 5.0, ...}
    ],
    'user1_recommends': [
        {'title': 'Inception', 'rating': 5.0, ...},
        {'title': 'Parasite', 'rating': 4.5, ...},
        # ... 18 more
    ],
    'user2_recommends': [
        {'title': 'Blade Runner', 'rating': 4.5, ...},
        {'title': 'Dune', 'rating': 5.0, ...},
        # ... 18 more
    ],
    'stats': {
        'user1_total': 150,
        'user2_total': 200,
        'common_movies': 45
    }
}
```

**Time taken**: < 1 second (very fast!)

---

## 🎬 Scene 7: Sending Response Back

**File**: `app.py`  
**Location**: Line 68

```python
return jsonify(recommendations)  # Converts Python dict to JSON string
```

**What happens**:
- Flask's `jsonify()` converts Python dictionary to JSON string
- JSON string sent as HTTP response body
- Response headers include: `Content-Type: application/json`
- Status code: 200 (success)

**JSON string sent** (simplified):
```json
{
  "both_enjoyed": [
    {"title": "The Matrix", "user1_rating": 4.5, "user2_rating": 5.0, ...}
  ],
  "user1_recommends": [...],
  "user2_recommends": [...],
  "stats": {"user1_total": 150, "user2_total": 200, "common_movies": 45}
}
```

---

## 🎬 Scene 8: Frontend Receives Response

**File**: `app.js`  
**Location**: Lines 50-65

```javascript
if (!response.ok) {
    throw new Error('Something went wrong');
}

const data = await response.json();  // Parses JSON string to JavaScript object
// data is now a JavaScript object matching the Python dictionary!

displayResults(data, user1, user2);
```

**What happens**:
- `response.json()` parses JSON string back to JavaScript object
- Now we have the data in JavaScript format
- Calls `displayResults()` to update the page

**JavaScript object** (same structure as Python dict):
```javascript
data = {
    both_enjoyed: [
        {title: "The Matrix", user1_rating: 4.5, user2_rating: 5.0, ...}
    ],
    user1_recommends: [...],
    user2_recommends: [...],
    stats: {user1_total: 150, user2_total: 200, common_movies: 45}
}
```

---

## 🎬 Scene 9: Displaying Results

**File**: `app.js`  
**Location**: Lines 70-120

```javascript
function displayResults(data, user1, user2) {
    // Update stats
    document.getElementById('user1Total').textContent = data.stats.user1_total;  // 150
    document.getElementById('user2Total').textContent = data.stats.user2_total;  // 200
    document.getElementById('commonMovies').textContent = data.stats.common_movies;  // 45
    
    // Display movies
    displayMovieList('bothEnjoyed', data.both_enjoyed, ...);
    displayMovieList('user1Recommends', data.user1_recommends, ...);
    displayMovieList('user2Recommends', data.user2_recommends, ...);
    
    showResults();  // Makes results section visible
}
```

**Creating Movie Cards**:
```javascript
function displayMovieList(containerId, movies, formatFn) {
    const container = document.getElementById('bothEnjoyed');
    container.innerHTML = '';  // Clear previous results
    
    movies.forEach(movie => {  // Loop through each movie
        const movieDiv = document.createElement('div');  // Create <div>
        movieDiv.className = 'movie-item';  // Add CSS class
        
        movieDiv.innerHTML = `
            <div class="movie-title">${movie.title}</div>
            <div class="movie-meta">
                <span class="movie-year">${movie.year}</span>
                <span class="movie-rating">⭐ ${movie.rating}/5</span>
                <a href="${movie.url}" class="movie-link">View on Letterboxd →</a>
            </div>
        `;
        
        container.appendChild(movieDiv);  // Add to page
    });
}
```

**What the user sees**:
- Stats card shows: "150 | 200 | 45"
- "Both Enjoyed" section shows movie cards
- "User 1 Recommends" section shows movie cards
- "User 2 Recommends" section shows movie cards
- Each card is clickable, links to Letterboxd

**Final UI state**:
- Loading spinner: Hidden
- Results section: Visible (with smooth fade-in animation)
- Button: Re-enabled, says "Find Matches" again

---

## 📊 Complete Timeline

```
0:00 - User clicks button
0:01 - Request sent to Flask
0:02 - Flask starts scraping user1
0:47 - User1 scraping complete (45 seconds)
0:48 - Flask starts scraping user2
1:38 - User2 scraping complete (50 seconds)
1:39 - Recommendations generated (< 1 second)
1:40 - Response sent to frontend
1:41 - Frontend updates page
1:42 - User sees results! 🎉
```

**Total time**: ~1 minute 42 seconds

---

## 🎓 Key Takeaways

1. **Asynchronous = Non-blocking**: JavaScript doesn't freeze during the wait
2. **Data Transformation**: HTML → Python Dict → JSON → JavaScript Object → HTML
3. **Set Operations**: Fast way to compare lists (intersection, difference)
4. **DOM Manipulation**: JavaScript creates HTML elements dynamically
5. **Error Handling**: Try/catch blocks handle failures gracefully

This is how modern web apps work - data flows through multiple layers, gets transformed at each step, and finally displayed to the user!

