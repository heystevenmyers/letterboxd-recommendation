"""
Recommendation Engine
This module contains the logic for generating movie recommendations

LEARNING NOTE: This uses collaborative filtering - comparing what users
have in common to make predictions about what they'll like.
"""
from collections import Counter
from letterboxd_scraper import get_movie_average_rating

def generate_recommendations(user1_movies, user2_movies, user1_watched=None, user2_watched=None):
    """
    Generates three types of recommendations:
    1. Movies both watched and enjoyed
    2. Movies one watched that the other would enjoy
    3. Movies neither has seen but would enjoy
    
    Args:
        user1_movies: Dict of {movie_title: {rating, year, url}} - rated movies (for comparisons)
        user2_movies: Dict of {movie_title: {rating, year, url}} - rated movies (for comparisons)
        user1_watched: Dict of {movie_title: {rating, year, url}} - all watched movies (for recommendations)
        user2_watched: Dict of {movie_title: {rating, year, url}} - all watched movies (for recommendations)
    
    Returns:
        Dictionary with recommendation categories
    """
    # Use watched lists if provided, otherwise fall back to rated lists
    if user1_watched is None:
        user1_watched = user1_movies
    if user2_watched is None:
        user2_watched = user2_movies
    
    # Convert to sets for easier comparison
    # Use rated movies for "both loved" and "both hated" comparisons
    user1_titles = set(user1_movies.keys())
    user2_titles = set(user2_movies.keys())
    
    # Use watched movies for checking "hasn't seen" in recommendations
    user1_watched_titles = set(user1_watched.keys())
    user2_watched_titles = set(user2_watched.keys())
    
    # 1. Movies both watched and enjoyed (4+ stars)
    both_watched = user1_titles & user2_titles
    both_enjoyed = []
    for title in both_watched:
        rating1 = user1_movies[title].get('rating')
        rating2 = user2_movies[title].get('rating')
        # Handle None values - convert to 0 for comparison
        rating1 = rating1 if rating1 is not None else 0
        rating2 = rating2 if rating2 is not None else 0
        # Both rated 4+ stars
        if rating1 >= 4.0 and rating2 >= 4.0:
            both_enjoyed.append({
                'title': title,
                'user1_rating': rating1,
                'user2_rating': rating2,
                'year': user1_movies[title].get('year'),
                'url': user1_movies[title].get('url')
            })
    
    # Sort and limit based on count
    if len(both_enjoyed) <= 10:
        # If 10 or fewer, prioritize both 5.0, then sort by Letterboxd average (lower = less popular)
        def get_sort_key(movie):
            r1 = movie['user1_rating']
            r2 = movie['user2_rating']
            
            # Group 1: Both 5.0 (highest priority)
            if r1 == 5.0 and r2 == 5.0:
                # Fetch Letterboxd average rating for sorting (lower = less popular = higher priority)
                letterboxd_avg = get_movie_average_rating(movie.get('url'))
                # Use 5.0 as default if we can't fetch (treat as popular)
                letterboxd_avg = letterboxd_avg if letterboxd_avg is not None else 5.0
                return (1, letterboxd_avg)  # Lower number = higher priority, lower avg = less popular
            # Group 2: One is 5.0, other is 4.5 or 4.0
            elif (r1 == 5.0 and r2 in [4.5, 4.0]) or (r2 == 5.0 and r1 in [4.5, 4.0]):
                letterboxd_avg = get_movie_average_rating(movie.get('url'))
                letterboxd_avg = letterboxd_avg if letterboxd_avg is not None else 5.0
                return (2, letterboxd_avg)
            # Group 3: Both are 4.5 or 4.0 (lowest priority within 4+ range)
            else:
                letterboxd_avg = get_movie_average_rating(movie.get('url'))
                letterboxd_avg = letterboxd_avg if letterboxd_avg is not None else 5.0
                return (3, letterboxd_avg)
        
        both_enjoyed.sort(key=get_sort_key)
    else:
        # If more than 10, prioritize and limit to 10
        def get_priority(movie):
            r1 = movie['user1_rating']
            r2 = movie['user2_rating']
            
            # Group 1: Both 5.0 (highest priority)
            if r1 == 5.0 and r2 == 5.0:
                # Fetch Letterboxd average rating for sorting (lower = less popular = higher priority)
                letterboxd_avg = get_movie_average_rating(movie.get('url'))
                # Use 5.0 as default if we can't fetch (treat as popular)
                letterboxd_avg = letterboxd_avg if letterboxd_avg is not None else 5.0
                return (1, letterboxd_avg)  # Lower number = higher priority, lower avg = less popular
            # Group 2: One is 5.0, other is 4.5 or 4.0
            elif (r1 == 5.0 and r2 in [4.5, 4.0]) or (r2 == 5.0 and r1 in [4.5, 4.0]):
                letterboxd_avg = get_movie_average_rating(movie.get('url'))
                letterboxd_avg = letterboxd_avg if letterboxd_avg is not None else 5.0
                return (2, letterboxd_avg)
            # Group 3: Both are 4.5 or 4.0 (lowest priority within 4+ range)
            else:
                letterboxd_avg = get_movie_average_rating(movie.get('url'))
                letterboxd_avg = letterboxd_avg if letterboxd_avg is not None else 5.0
                return (3, letterboxd_avg)
        
        both_enjoyed.sort(key=get_priority)
        both_enjoyed = both_enjoyed[:10]  # Limit to 10
    
    # 1b. Movies both hated (1.0 or 0.5 stars only - exclude 0.0 and None)
    # Letterboxd doesn't recognize 0 stars as a valid rating
    both_hated = []
    for title in both_watched:
        rating1 = user1_movies[title].get('rating')
        rating2 = user2_movies[title].get('rating')
        # Exclude if either rating is None (as per plan)
        if rating1 is not None and rating2 is not None:
            # Both rated 1.0 or below, but exclude 0.0 (only 0.5 and 1.0)
            if rating1 > 0.0 and rating1 <= 1.0 and rating2 > 0.0 and rating2 <= 1.0:
                both_hated.append({
                    'title': title,
                    'user1_rating': rating1,
                    'user2_rating': rating2,
                    'year': user1_movies[title].get('year'),
                    'url': user1_movies[title].get('url')
                })
    
    # Sort by average rating (lowest first - worst movies at top)
    both_hated.sort(key=lambda x: ((x['user1_rating'] or 0) + (x['user2_rating'] or 0)) / 2)
    both_hated = both_hated[:10]  # Limit to 10
    
    # 2. Movies user1 watched that user2 would enjoy
    # Find movies user1 ranked 4.5 or 5 that user2 hasn't seen
    user1_recommends = []
    for title, data in user1_movies.items():
        rating = data.get('rating')
        # Handle None values
        rating = rating if rating is not None else 0
        # Filter for movies rated 4.5 or 5.0 (4.5+)
        # Check if user2 hasn't watched it (using watched list)
        if title not in user2_watched_titles and rating >= 4.5:
            user1_recommends.append({
                'title': title,
                'rating': rating,
                'year': data.get('year'),
                'url': data.get('url')
            })
    
    user1_recommends.sort(key=lambda x: x['rating'] or 0, reverse=True)
    user1_recommends = user1_recommends[:10]  # Top 10
    
    # 3. Movies user2 watched that user1 would enjoy
    # Find movies user2 ranked 4.5 or 5 that user1 hasn't seen
    user2_recommends = []
    for title, data in user2_movies.items():
        rating = data.get('rating')
        # Handle None values
        rating = rating if rating is not None else 0
        # Filter for movies rated 4.5 or 5.0 (4.5+)
        # Check if user1 hasn't watched it (using watched list)
        if title not in user1_watched_titles and rating >= 4.5:
            user2_recommends.append({
                'title': title,
                'rating': rating,
                'year': data.get('year'),
                'url': data.get('url')
            })
    
    user2_recommends.sort(key=lambda x: x['rating'] or 0, reverse=True)
    user2_recommends = user2_recommends[:10]  # Top 10
    
    # 4. Movies neither has seen but would enjoy (AI-powered)
    new_suggestions = []
    
    # Filter for movies both rated exactly 5.0 stars
    both_5star = []
    for movie in both_enjoyed:
        rating1 = movie.get('user1_rating', 0)
        rating2 = movie.get('user2_rating', 0)
        if rating1 == 5.0 and rating2 == 5.0:
            both_5star.append(movie)
    
    # Only use AI if we have at least 3 movies both rated 5.0
    if len(both_5star) >= 3:
        try:
            from ai_recommender import get_ai_recommendations
            new_suggestions = get_ai_recommendations(
                both_5star,
                user1_watched,
                user2_watched
            )
            # Limit to 10
            new_suggestions = new_suggestions[:10]
        except Exception as e:
            print(f"Error getting AI recommendations: {e}")
            new_suggestions = []
    
    # Calculate common movies from watched lists (not just rated)
    both_watched_all = user1_watched_titles & user2_watched_titles
    
    return {
        'both_enjoyed': both_enjoyed,
        'both_hated': both_hated,
        'user1_recommends': user1_recommends,
        'user2_recommends': user2_recommends,
        'new_suggestions': new_suggestions,
        'stats': {
            'user1_total': len(user1_watched),
            'user2_total': len(user2_watched),
            'common_movies': len(both_watched_all)
        }
    }

