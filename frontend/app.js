/**
 * Frontend JavaScript
 * 
 * LEARNING NOTE: This handles user interactions and communicates
 * with our backend API using fetch() - the modern way to make HTTP requests
 * 
 * VERCEL NOTE: Uses environment variables for API URL configuration
 */

// API endpoint - uses environment variable or falls back to localhost
// Vercel will inject VITE_API_URL or NEXT_PUBLIC_API_URL at build time
// For vanilla JS, we'll use a config approach
const getApiUrl = () => {
    // Check for environment variable (Vercel injects these)
    if (typeof window !== 'undefined' && window.API_URL) {
        return window.API_URL;
    }
    
    // Always use relative URL when on same origin (localhost or 127.0.0.1)
    // This avoids CORS issues completely
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        return '/api/analyze';  // Relative URL - same origin, no CORS issues
    }
    
    // Check for meta tag (for production/Vercel deployments)
    const metaTag = document.querySelector('meta[name="api-url"]');
    if (metaTag) {
        const url = metaTag.getAttribute('content');
        // If meta tag is relative, use it; if absolute, use it
        return url.startsWith('/') ? url : url;
    }
    
    // Fallback: use relative URL based on current location
    return '/api/analyze';
};

const API_URL = getApiUrl();

// Get references to DOM elements
const form = document.getElementById('userForm');
const submitBtn = document.getElementById('submitBtn');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');

/**
 * Handle form submission
 */
form.addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent page refresh
    
    // Get form values
    const user1 = document.getElementById('user1').value.trim();
    const user2 = document.getElementById('user2').value.trim();
    
    if (!user1) {
        showError('Please enter at least one username');
        return;
    }
    
    // Show loading, hide other sections
    showLoading();
    hideResults();
    hideError();
    
    try {
        // Make API request to our backend
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
        
        // Check if request was successful
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Something went wrong');
        }
        
        // Parse JSON response
        const data = await response.json();
        
        // Display results
        displayResults(data, user1, user2);
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'Failed to fetch data. Make sure the server is running!');
    } finally {
        hideLoading();
    }
});

/**
 * Display the recommendation results
 */
function displayResults(data, user1, user2) {
    // Update user names in the UI
    document.getElementById('user1Name').textContent = user1;
    document.getElementById('user1NameRec').textContent = user1;
    document.getElementById('user1NameDesc').textContent = user1;
    document.getElementById('user1NameDescRec').textContent = user1;
    document.getElementById('user1StatLabel').textContent = user1;
    
    if (user2) {
        document.getElementById('user2Name').textContent = user2;
        document.getElementById('user2NameRec').textContent = user2;
        document.getElementById('user2NameDesc').textContent = user2;
        document.getElementById('user2NameDescRec').textContent = user2;
        document.getElementById('user2StatLabel').textContent = user2;
    } else {
        document.getElementById('user2Name').textContent = 'User 2';
        document.getElementById('user2NameRec').textContent = 'User 2';
        document.getElementById('user2NameDesc').textContent = 'User 2';
        document.getElementById('user2NameDescRec').textContent = 'User 2';
        document.getElementById('user2StatLabel').textContent = 'User 2';
    }
    
    // Display stats
    if (data.stats) {
        document.getElementById('user1Total').textContent = data.stats.user1_total || 0;
        document.getElementById('user2Total').textContent = data.stats.user2_total || 0;
        document.getElementById('commonMovies').textContent = data.stats.common_movies || 0;
    }
    
    // Display both enjoyed movies
    displayMovieList('bothEnjoyed', data.both_enjoyed || [], (movie) => {
        return `${movie.title}${movie.year ? ` (${movie.year})` : ''} - 
                ⭐ ${movie.user1_rating}/5 & ${movie.user2_rating}/5`;
    });
    
    // Display both hated movies
    displayMovieList('bothHated', data.both_hated || [], (movie) => {
        return `${movie.title}${movie.year ? ` (${movie.year})` : ''} - 
                ⭐ ${movie.user1_rating}/5 & ${movie.user2_rating}/5`;
    });
    
    // Display user1 recommendations
    displayMovieList('user1Recommends', data.user1_recommends || [], (movie) => {
        return `${movie.title}${movie.year ? ` (${movie.year})` : ''} - ⭐ ${movie.rating}/5`;
    });
    
    // Display user2 recommendations
    displayMovieList('user2Recommends', data.user2_recommends || [], (movie) => {
        return `${movie.title}${movie.year ? ` (${movie.year})` : ''} - ⭐ ${movie.rating}/5`;
    });
    
    // Display new suggestions (AI recommendations)
    displayMovieList('newSuggestions', data.new_suggestions || [], (movie) => {
        return `${movie.title}${movie.year ? ` (${movie.year})` : ''}${movie.reason ? ` - ${movie.reason}` : ''}`;
    });
    
    // Show results section
    showResults();
}

/**
 * Helper function to display a list of movies
 */
function displayMovieList(containerId, movies, formatFn) {
    const container = document.getElementById(containerId);
    container.innerHTML = ''; // Clear previous results
    
    if (movies.length === 0) {
        container.innerHTML = '<p class="empty-state">No movies found in this category.</p>';
        return;
    }
    
    movies.forEach(movie => {
        const movieDiv = document.createElement('div');
        movieDiv.className = 'movie-item';
        
        // Handle ratings display
        let ratingDisplay = '';
        if (movie.user1_rating !== null && movie.user1_rating !== undefined && 
            movie.user2_rating !== null && movie.user2_rating !== undefined) {
            // Both ratings available
            ratingDisplay = `
                <span class="movie-rating">User 1: ⭐ ${movie.user1_rating}/5</span>
                <span class="movie-rating">User 2: ⭐ ${movie.user2_rating}/5</span>
            `;
        } else if (movie.user1_rating !== null && movie.user1_rating !== undefined) {
            // Only user1 rating
            ratingDisplay = `<span class="movie-rating">User 1: ⭐ ${movie.user1_rating}/5</span>`;
        } else if (movie.user2_rating !== null && movie.user2_rating !== undefined) {
            // Only user2 rating
            ratingDisplay = `<span class="movie-rating">User 2: ⭐ ${movie.user2_rating}/5</span>`;
        } else if (movie.rating !== null && movie.rating !== undefined) {
            // Single rating (for recommendations)
            ratingDisplay = `<span class="movie-rating">⭐ ${movie.rating}/5</span>`;
        } else {
            // No ratings
            ratingDisplay = '<span class="movie-rating">No rating</span>';
        }
        
        const movieLink = movie.url || '#';
        
        movieDiv.innerHTML = `
            <div class="movie-info">
                <a href="${movieLink}" target="_blank" class="movie-title-link">
                    <div class="movie-title">${movie.title}</div>
                </a>
                <div class="movie-meta">
                    ${movie.year ? `<span class="movie-year">${movie.year}</span>` : ''}
                    ${ratingDisplay}
                </div>
                ${movie.reason ? `<div class="movie-reason">${movie.reason}</div>` : ''}
            </div>
        `;
        
        container.appendChild(movieDiv);
    });
}

/**
 * Show/hide helper functions
 */
function showLoading() {
    loadingSection.classList.remove('hidden');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Analyzing...';
}

function hideLoading() {
    loadingSection.classList.add('hidden');
    submitBtn.disabled = false;
    submitBtn.textContent = 'Find Matches';
}

function showResults() {
    resultsSection.classList.remove('hidden');
}

function hideResults() {
    resultsSection.classList.add('hidden');
}

function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    errorSection.classList.remove('hidden');
}

function hideError() {
    errorSection.classList.add('hidden');
}

function resetForm() {
    hideError();
    hideResults();
    form.reset();
}
