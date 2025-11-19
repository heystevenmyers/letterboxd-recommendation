"""
AI-Powered Movie Recommendation Module
Uses Claude (Anthropic) to analyze movies and generate recommendations
"""
import os
import json
import re
from anthropic import Anthropic
from dotenv import load_dotenv
import pathlib

# Load environment variables from .env file in project root
project_root = pathlib.Path(__file__).parent.parent
load_dotenv(dotenv_path=project_root / '.env')

def get_ai_recommendations(both_5star_movies, user1_watched, user2_watched):
    """
    Uses Claude AI to analyze movies both users rated 5 stars and generate recommendations
    
    Args:
        both_5star_movies: List of movies both users rated exactly 5.0 stars
        user1_watched: Dict of all movies user1 has watched
        user2_watched: Dict of all movies user2 has watched
    
    Returns:
        List of recommended movies with title, year, reason, and url
    """
    # Check if API key is available
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("Warning: ANTHROPIC_API_KEY not set. Skipping AI recommendations.")
        return []
    
    # Validate API key format (should start with sk-ant-)
    if not api_key.startswith('sk-ant-'):
        print("Warning: ANTHROPIC_API_KEY appears to be invalid (should start with 'sk-ant-'). Skipping AI recommendations.")
        return []
    
    try:
        # Initialize Anthropic client
        client = Anthropic(api_key=api_key)
        
        # Format movie list for prompt
        movie_list = []
        for movie in both_5star_movies:
            title = movie.get('title', '')
            year = movie.get('year', '')
            if year:
                movie_list.append(f"- {title} ({year})")
            else:
                movie_list.append(f"- {title}")
        
        # Format watched movies list (combined, to exclude from recommendations)
        all_watched_titles = set(user1_watched.keys()) | set(user2_watched.keys())
        watched_list = []
        for title in sorted(all_watched_titles)[:100]:  # Limit to first 100 to avoid token limits
            watched_list.append(f"- {title}")
        
        # Create prompt
        prompt = f"""You are a movie recommendation expert. Analyze the following movies that two users both rated 5 stars:

{chr(10).join(movie_list)}

Both users have already watched these movies (do not recommend these):
{chr(10).join(watched_list[:50])}

IMPORTANT: 
1. Analyze the 5-star movies to find common themes in actors, genres, directors, composers, cinematographers, etc.
2. Truly hone in on the themes and connections between the movies - don't just suggest movies that are similar to the ones the users have already watched
3. Avoid the obvious answers, shy away from the most popular movies and lean towards obscure movies
4. Focus on patterns and connections between the movies - ignore outliers that don't fit clear themes
5. Based on these common themes, suggest 10 movies they would both enjoy that they haven't seen yet
6. Its common for users to not rate movies they have seen. do not reccomend a very popular movie even if it is not on either persons watched list.

Format your response as a JSON array: [{{"title": "Movie Title", "year": 2023, "reason": "why they'd like it based on the themes"}}]"""

        # Call Claude API - try multiple models in order of preference
        models_to_try = [
            "claude-3-7-sonnet-20250219",  # Latest Sonnet model
            "claude-3-5-haiku-latest",     # Fallback to Haiku
            "claude-3-opus-latest",        # Fallback to Opus
        ]
        
        message = None
        last_error = None
        
        for model_name in models_to_try:
            try:
                message = client.messages.create(
                    model=model_name,
                    max_tokens=2000,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    timeout=60.0  # 60 second timeout
                )
                print(f"DEBUG: Successfully used model: {model_name}")
                break  # Success, exit the loop
            except Exception as e:
                last_error = e
                error_str = str(e)
                # Check for model not found errors (404)
                if '404' in error_str or 'not_found' in error_str.lower() or ('error' in error_str.lower() and 'model' in error_str.lower()):
                    print(f"DEBUG: Model {model_name} not available, trying next...")
                    continue  # Try next model
                else:
                    # For other errors (like auth), don't try other models
                    raise  # Re-raise if it's not a 404/model not found error
        
        if message is None:
            raise Exception(f"None of the available models worked. Last error: {last_error}")
        
        # Extract response text
        response_text = message.content[0].text
        print(f"DEBUG: AI response received (length: {len(response_text)})")
        
        # Parse JSON from response (may be wrapped in markdown code blocks)
        json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                recommendations = json.loads(json_str)
                
                # Convert to our format and add Letterboxd URLs
                result = []
                for rec in recommendations[:10]:  # Limit to 10
                    title = rec.get('title', '')
                    year = rec.get('year', '')
                    reason = rec.get('reason', '')
                    
                    # Construct Letterboxd URL (basic format)
                    film_slug = title.lower().replace(' ', '-').replace("'", '').replace(':', '').replace(',', '')
                    film_slug = re.sub(r'[^a-z0-9-]', '', film_slug)
                    url = f"https://letterboxd.com/film/{film_slug}/"
                    
                    result.append({
                        'title': title,
                        'year': year,
                        'reason': reason,
                        'url': url
                    })
                
                print(f"DEBUG: Successfully parsed {len(result)} recommendations")
                return result
            except json.JSONDecodeError as e:
                print(f"ERROR: Failed to parse JSON: {e}")
                print(f"DEBUG: JSON string: {json_str[:500]}")
                return []
        else:
            print("Warning: Could not find JSON array in AI response")
            print(f"DEBUG: Response text: {response_text[:500]}")
            return []
            
    except Exception as e:
        error_str = str(e)
        # Check for authentication errors
        if '401' in error_str or 'authentication' in error_str.lower() or 'invalid' in error_str.lower() and 'api-key' in error_str.lower():
            print("Error: Invalid Anthropic API key. Please check your .env file:")
            print("  1. Make sure ANTHROPIC_API_KEY is set correctly")
            print("  2. Get a new key from https://console.anthropic.com/")
            print("  3. Ensure the key starts with 'sk-ant-'")
            print("  4. Make sure there are no extra spaces or quotes in the .env file")
        else:
            print(f"Error getting AI recommendations: {e}")
        return []


