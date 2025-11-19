"""
Letterboxd Scraper Module
This module handles fetching and parsing data from Letterboxd profiles

LEARNING NOTE: Web scraping extracts data from HTML pages.
We're using BeautifulSoup to parse the HTML structure.
"""
import requests
from bs4 import BeautifulSoup
import time
import re
import json

def get_user_movies(username):
    """
    Fetches all movies a user has rated from their Letterboxd profile
    
    Uses the /films/rated/{rating}/ pages which show movies by rating.
    Loops through all ratings from 0.5 to 5.0 in 0.5 increments.
    
    Args:
        username: Letterboxd username
    
    Returns:
        Dictionary with movie data: {
            'movie_title': {
                'rating': 4.5,  # 0.5-5.0 based on page URL
                'year': 2023,
                'url': 'https://...'
            }
        }
    """
    movies = {}
    
    # Only fetch ratings we actually need:
    # - 0.5, 1.0 for "both hated" section
    # - 4.0, 4.5, 5.0 for "both loved" section and recommendations
    # This reduces scraping time by 50% (5 ratings instead of 10)
    ratings = [0.5, 1.0, 4.0, 4.5, 5.0]
    
    for rating_value in ratings:
        page = 1
        max_pages = 100  # Safety limit to prevent infinite loops
        
        print(f"  Fetching movies rated {rating_value}...")
        
        # Loop through all pages for this rating
        while page <= max_pages:
            # Construct URL - Letterboxd uses /films/rated/{rating}/ for movies by rating
            # Format: whole numbers use integer (5), half-stars use decimal (4.5)
            if rating_value == int(rating_value):
                url = f"https://letterboxd.com/{username}/films/rated/{int(rating_value)}/page/{page}/"
            else:
                url = f"https://letterboxd.com/{username}/films/rated/{rating_value}/page/{page}/"
            
            try:
                # Add headers to look like a real browser
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(url, headers=headers, timeout=10)
                
                if response.status_code != 200:
                    # If page doesn't exist, we've reached the end
                    break
                
                soup = BeautifulSoup(response.content, 'lxml')
                
                # Find all movie entries on the page
                # Letterboxd uses <div class="poster film-poster"> for movies
                movie_elements = soup.find_all('div', class_='poster')
                
                # Alternative: try finding by film-poster class
                if not movie_elements:
                    movie_elements = soup.find_all('div', class_='film-poster')
                
                # Fallback: try old selectors for compatibility
                if not movie_elements:
                    movie_elements = soup.find_all('li', class_='posteritem')
                if not movie_elements:
                    movie_elements = soup.find_all('div', {'data-film-id': True})
                if not movie_elements:
                    movie_elements = soup.find_all('li', class_='poster-container')
                
                if not movie_elements:
                    # No more movies on this page for this rating
                    break
                
                movies_found_on_page = 0
                for element in movie_elements:
                    # Extract movie title from the img alt text or data attribute
                    img = element.find('img')
                    if not img:
                        continue
                    
                    # Get movie title - try multiple methods
                    title = None
                    # Try link's data-original-title first (cleanest)
                    link = element.find('a')
                    if link:
                        title = link.get('data-original-title', '').strip()
                    
                    # Try img alt text (may have "Poster for" prefix)
                    if not title:
                        title = img.get('alt', '').strip()
                        # Remove "Poster for" prefix if present
                        if title.startswith('Poster for '):
                            title = title.replace('Poster for ', '', 1).strip()
                    
                    # Try img title attribute
                    if not title:
                        title = img.get('title', '').strip()
                    
                    # Try data attribute
                    if not title:
                        title = element.get('data-film-name', '').strip()
                    
                    if not title:
                        continue
                    
                    # Get movie URL (link was already found above)
                    if not link:
                        link = element.find('a')
                    if link and link.get('href'):
                        movie_url = f"https://letterboxd.com{link.get('href')}"
                    else:
                        movie_url = None
                    
                    # Extract year if available
                    year = None
                    year_match = re.search(r'\((\d{4})\)', title)
                    if year_match:
                        year = int(year_match.group(1))
                        title = title.replace(f'({year})', '').strip()
                    
                    # Also try to get year from data attribute
                    if not year:
                        year_attr = element.get('data-film-year', '')
                        if year_attr:
                            try:
                                year = int(year_attr)
                            except:
                                pass
                    
                    # Store movie with the rating from the URL
                    # We know the rating because we're on the /films/rated/{rating}/ page
                    movies[title] = {
                        'rating': rating_value,  # Rating from URL
                        'year': year,
                        'url': movie_url
                    }
                    movies_found_on_page += 1
                
                # If no movies found on this page, we've reached the end
                if movies_found_on_page == 0:
                    break
                
                page += 1
                time.sleep(0.5)  # Be polite - wait 0.5 seconds between requests (optimized for speed)
                
            except requests.exceptions.Timeout:
                print(f"  Timeout fetching page {page} for rating {rating_value}")
                break
            except requests.exceptions.RequestException as e:
                print(f"  Network error fetching page {page} for rating {rating_value}: {e}")
                break
            except Exception as e:
                print(f"  Error fetching page {page} for rating {rating_value}: {e}")
                break
    
    # Check if we found any movies at all
    if len(movies) == 0:
        raise Exception(f"User '{username}' not found or has no rated movies")
    
    print(f"Found {len(movies)} movies for {username} ({sum(1 for m in movies.values() if m.get('rating') is not None)} with ratings)")
    return movies

def get_user_watched_movies(username):
    """
    Fetches all movies a user has watched from their Letterboxd profile
    
    Uses the /films/ page which shows all watched movies (rated and unrated).
    Extracts ratings by counting star characters (★) in the HTML if available.
    
    Args:
        username: Letterboxd username
    
    Returns:
        Dictionary with movie data: {
            'movie_title': {
                'rating': 4.5,  # 0.5-5.0 if rated, or None if unrated
                'year': 2023,
                'url': 'https://...'
            }
        }
    """
    movies = {}
    page = 1
    max_pages = 100  # Safety limit to prevent infinite loops
    
    print(f"  Fetching watched movies...")
    
    # Loop through all pages of watched films
    while page <= max_pages:
        # Construct URL - Letterboxd uses /films/ for all watched movies
        url = f"https://letterboxd.com/{username}/films/page/{page}/"
        
        try:
            # Add headers to look like a real browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                # If page doesn't exist, we've reached the end
                if page == 1:
                    raise Exception(f"User '{username}' not found or has no watched movies")
                break
            
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Find all movie entries on the page
            # Letterboxd uses <div class="poster film-poster"> for movies
            movie_elements = soup.find_all('div', class_='poster')
            
            # Alternative: try finding by film-poster class
            if not movie_elements:
                movie_elements = soup.find_all('div', class_='film-poster')
            
            # Fallback: try old selectors for compatibility
            if not movie_elements:
                movie_elements = soup.find_all('li', class_='posteritem')
            if not movie_elements:
                movie_elements = soup.find_all('div', {'data-film-id': True})
            if not movie_elements:
                movie_elements = soup.find_all('li', class_='poster-container')
            
            if not movie_elements:
                # No more movies on this page
                if page == 1:
                    raise Exception(f"User '{username}' not found or has no watched movies")
                break  # Reached last page
            
            movies_found_on_page = 0
            
            for element in movie_elements:
                # Extract movie title from the img alt text or data attribute
                img = element.find('img')
                if not img:
                    continue
                
                # Get movie title - try multiple methods
                title = None
                # Try link's data-original-title first (cleanest)
                link = element.find('a')
                if link:
                    title = link.get('data-original-title', '').strip()
                
                # Try img alt text (may have "Poster for" prefix)
                if not title:
                    title = img.get('alt', '').strip()
                    # Remove "Poster for" prefix if present
                    if title.startswith('Poster for '):
                        title = title.replace('Poster for ', '', 1).strip()
                
                # Try img title attribute
                if not title:
                    title = img.get('title', '').strip()
                
                # Try data attribute
                if not title:
                    title = element.get('data-film-name', '').strip()
                
                if not title:
                    continue
                
                # Get movie URL (link was already found above)
                if not link:
                    link = element.find('a')
                if link and link.get('href'):
                    movie_url = f"https://letterboxd.com{link.get('href')}"
                else:
                    movie_url = None
                
                # Try to find rating by counting star characters (★) in the HTML
                # Letterboxd displays ratings as star symbols: ★★★★★ = 5.0, ★★★★ = 4.0, etc.
                rating = None
                
                # First, look for poster-viewingdata paragraph
                viewing_data = element.find('p', class_='poster-viewingdata')
                if viewing_data:
                    # Find span with 'rating' in class list
                    rating_span = viewing_data.find('span', class_=lambda x: x and 'rating' in x)
                    if rating_span:
                        # Get text content and count star characters
                        rating_text = rating_span.get_text()
                        star_count = rating_text.count('★')
                        if star_count > 0:
                            rating = float(star_count)
                            # Check for half-star (½ or similar)
                            if '½' in rating_text or '1/2' in rating_text.lower():
                                rating += 0.5
                
                # Fallback: search for stars anywhere in the element
                if not rating:
                    element_text = element.get_text()
                    star_count = element_text.count('★')
                    if star_count > 0 and star_count <= 5:
                        rating = float(star_count)
                        # Check for half-star
                        if '½' in element_text or '1/2' in element_text.lower():
                            rating += 0.5
                
                # Also try finding rating span directly in element (another fallback)
                if not rating:
                    rating_span = element.find('span', class_=lambda x: x and 'rating' in x)
                    if rating_span:
                        rating_text = rating_span.get_text()
                        star_count = rating_text.count('★')
                        if star_count > 0:
                            rating = float(star_count)
                            if '½' in rating_text or '1/2' in rating_text.lower():
                                rating += 0.5
                
                # Extract year if available
                year = None
                year_match = re.search(r'\((\d{4})\)', title)
                if year_match:
                    year = int(year_match.group(1))
                    title = title.replace(f'({year})', '').strip()
                
                # Also try to get year from data attribute
                if not year:
                    year_attr = element.get('data-film-year', '')
                    if year_attr:
                        try:
                            year = int(year_attr)
                        except:
                            pass
                
                # Store movie with rating (can be None if unrated)
                # Exclude 0.0 ratings (Letterboxd doesn't recognize 0 stars as valid)
                if rating is not None and rating > 0.0:
                    movies[title] = {
                        'rating': rating,  # 0.5-5.0
                        'year': year,
                        'url': movie_url
                    }
                    movies_found_on_page += 1
                elif rating is None:
                    # Store unrated movies as None
                    movies[title] = {
                        'rating': None,
                        'year': year,
                        'url': movie_url
                    }
                    movies_found_on_page += 1
                # If rating is 0.0, don't store it (skip this movie)
            
            # If no movies found on this page, we've reached the end
            if movies_found_on_page == 0:
                break
            
            page += 1
            time.sleep(0.5)  # Be polite - wait 0.5 seconds between requests (optimized for speed)
            
        except requests.exceptions.Timeout:
            print(f"  Timeout fetching watched movies page {page}")
            break
        except requests.exceptions.RequestException as e:
            print(f"  Network error fetching watched movies page {page}: {e}")
            break
        except Exception as e:
            print(f"  Error fetching watched movies page {page}: {e}")
            break
    
    print(f"Found {len(movies)} watched movies for {username} ({sum(1 for m in movies.values() if m.get('rating') is not None)} with ratings)")
    return movies

def get_movie_average_rating(movie_url):
    """
    Fetches the Letterboxd average rating for a movie
    Returns the average rating as a float, or None if not found
    """
    if not movie_url:
        return None
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(movie_url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Letterboxd displays average rating in various places
        # Try to find it in multiple locations
        average_rating = None
        
        # Method 1: Look for meta tag with property="letterboxd:filmRating"
        meta_rating = soup.find('meta', {'property': 'letterboxd:filmRating'})
        if meta_rating and meta_rating.get('content'):
            try:
                average_rating = float(meta_rating.get('content'))
            except:
                pass
        
        # Method 2: Look for rating in the film-rating section
        if not average_rating:
            rating_section = soup.find('div', class_='film-rating')
            if rating_section:
                rating_text = rating_section.get_text()
                # Extract number from text like "3.8" or "3.8/5"
                rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                if rating_match:
                    try:
                        average_rating = float(rating_match.group(1))
                    except:
                        pass
        
        # Method 3: Look for data attribute
        if not average_rating:
            rating_elem = soup.find(attrs={'data-average-rating': True})
            if rating_elem:
                try:
                    average_rating = float(rating_elem.get('data-average-rating'))
                except:
                    pass
        
        # Method 4: Look for average rating in script tags (JSON-LD)
        if not average_rating:
            scripts = soup.find_all('script', type='application/ld+json')
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    if isinstance(data, dict) and 'aggregateRating' in data:
                        rating_value = data['aggregateRating'].get('ratingValue')
                        if rating_value:
                            average_rating = float(rating_value)
                            break
                except:
                    continue
        
        return average_rating
    except Exception as e:
        # Silently fail - we'll use default value
        return None

def get_movie_details(movie_url):
    """
    Fetches additional details about a movie (genres, director, etc.)
    Useful for better recommendations later
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(movie_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Extract genres, director, etc. (you can expand this)
        details = {}
        # Add more parsing logic here as needed
        
        return details
    except:
        return {}

