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
1. Analyze the 5-star movies to find common themes (actors, genres, directors, production companies, composers, cinematographers, etc.)
2. Focus on patterns and connections between the movies - ignore outliers that don't fit clear themes
3. Based on these common themes, suggest 10 movies they would both enjoy that they haven't seen yet
4. Make sure the suggested movies align with the themes you identified

Format your response as a JSON array: [{{"title": "Movie Title", "year": 2023, "reason": "why they'd like it based on the themes"}}]"""

        # Call Claude API
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            timeout=60.0  # 60 second timeout
        )
        
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
        print(f"Error getting AI recommendations: {e}")
        return []


