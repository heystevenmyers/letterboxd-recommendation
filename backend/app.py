"""
Flask Backend Server
This handles API requests and scrapes Letterboxd data
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from letterboxd_scraper import get_user_movies, get_user_watched_movies, get_movie_details
from recommender import generate_recommendations
from dotenv import load_dotenv
import pathlib

# Load environment variables from .env file in project root
project_root = pathlib.Path(__file__).parent.parent
load_dotenv(dotenv_path=project_root / '.env')

app = Flask(__name__, static_folder='../frontend', static_url_path='')
# Configure CORS to allow all origins (for development)
# In production, you'd want to restrict this to your actual domain
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Allowed static file extensions
ALLOWED_EXTENSIONS = {'.html', '.css', '.js', '.json', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico'}

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS) - only allow safe file types"""
    # Only serve files with allowed extensions
    if any(path.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        return send_from_directory('../frontend', path)
    return jsonify({'error': 'File not found'}), 404

@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def analyze_users():
    """
    Main API endpoint that takes two usernames and returns recommendations
    
    POST body: {
        "user1": "username1",
        "user2": "username2" (optional)
    }
    """
    # Handle preflight requests
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
    
    data = request.json
    user1 = data.get('user1')
    user2 = data.get('user2')
    
    if not user1:
        return jsonify({'error': 'At least one username required'}), 400
    
    try:
        # Fetch rated movies for user(s) (used for "both loved" and "both hated")
        print(f"Fetching rated movies for {user1}...")
        user1_movies = get_user_movies(user1)
        
        # Fetch watched movies for user(s) (used for recommendations)
        print(f"Fetching watched movies for {user1}...")
        user1_watched = get_user_watched_movies(user1)
        
        if user2:
            print(f"Fetching rated movies for {user2}...")
            user2_movies = get_user_movies(user2)
            print(f"Fetching watched movies for {user2}...")
            user2_watched = get_user_watched_movies(user2)
            # Generate recommendations comparing both users
            recommendations = generate_recommendations(user1_movies, user2_movies, user1_watched, user2_watched)
        else:
            # Single user mode - just return their data
            recommendations = {
                'both_enjoyed': [],
                'user1_recommends': [],
                'user2_recommends': [],
                'new_suggestions': [],
                'user1_movies': user1_movies
            }
        
        return jsonify(recommendations)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Simple health check endpoint"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("Starting Letterboxd Recommendation Server...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)

