from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from models import db, User, MoodRecord, Song
from config import Config
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError




load_dotenv()
app = Flask(__name__)

app.config.from_object(Config)
CORS(app)
db.init_app(app)
bcrypt = Bcrypt(app)

import requests
from urllib.parse import quote
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'connect_args': {
        'keepalives': 1,
        'keepalives_idle': 30,
        'keepalives_interval': 10,
        'keepalives_count': 5,
        'connect_timeout': 10
    }
}

def setup_spotify_client():
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        raise ValueError("Spotify credentials not found in environment variables.")
    
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id, 
        client_secret=client_secret
    )
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)


spotify_client = setup_spotify_client()

def setup_gemini():
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    if not GOOGLE_API_KEY:
        raise ValueError("API key not found in environment variables.")
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro')
    return model

model = setup_gemini()

def get_youtube_link(song_title):
   
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    
    if not YOUTUBE_API_KEY:
        raise ValueError("YouTube API key not found in environment variables.")
    
    base_url = "https://www.googleapis.com/youtube/v3/search"
    search_query = f"{song_title} official music video"
    
    params = {
        'part': 'snippet',
        'q': search_query,
        'key': YOUTUBE_API_KEY,
        'maxResults': 1,
        'type': 'video',
        'videoEmbeddable': 'true'
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            video_id = data['items'][0]['id']['videoId']
            return f"https://www.youtube.com/watch?v={video_id}"
        else:
            return None
    except Exception as e:
        print(f"Error fetching YouTube link: {e}")
        return None

def get_spotify_link(song_title, artist):
   
    try:
        # Search for the track
        results = spotify_client.search(q=f'track:{song_title} artist:{artist}', type='track', limit=1)
        
        # Extract track information
        tracks = results.get('tracks', {}).get('items', [])
        
        if tracks:
            track = tracks[0]
            return {
                'spotifyLink': track['external_urls']['spotify'],
                'previewUrl': track.get('preview_url'),
                'fullTrackName': f"{track['name']} - {track['artists'][0]['name']}"
            }
        return None
    except Exception as e:
        print(f"Error fetching Spotify link: {e}")
        return None

def get_time_of_day(hour):
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 22:
        return "evening"
    else:
        return "night"

def create_prompt(mood, hour):
    time_of_day = get_time_of_day(hour)
    return f"""As an expert in viral songs, provide personalized recommendations for someone feeling {mood} during the {time_of_day} (current hour: {hour}:00).
Please suggest:
1. A specific type of cuisine or dish that complements their emotional state.
2. 5 specific songs with their full titles including artist names that match the mood.
3. A brief explanation in about 150 to 200 characters of why these recommendations are beneficial.

Format the response as a JSON object with the following structure:
{{
  "cuisine": "Recommended cuisine or dish",
  "songs": [
    {{"title": "Song Title 1 - Artist Name"}},
    {{"title": "Song Title 2 - Artist Name"}},
    {{"title": "Song Title 3 - Artist Name"}},
    {{"title": "Song Title 4 - Artist Name"}},
    {{"title": "Song Title 5 - Artist Name"}}
  ],
  "explanation": "Brief explanation of why these recommendations are beneficial"
}}"""

def get_recommendations(model, mood, hour):
   

    prompt = create_prompt(mood, hour)
    response = model.generate_content(prompt)
    
    try:
        content = response.text
        cleaned_content = content.strip().strip("```json").strip("```")
        recommendations = json.loads(cleaned_content)
        
        # Add YouTube and Spotify links to songs
        songs_with_links = []
        for song in recommendations['songs']:
            # Split title into song and artist
            title_parts = song['title'].split(' - ')
            song_title = title_parts[0]
            artist = title_parts[1] if len(title_parts) > 1 else ''
            
            # Get links
            youtube_link = get_youtube_link(song_title)
            spotify_data = get_spotify_link(song_title, artist)
            
            song_info = {
                'title': song['title'],
                'youtubeLink': youtube_link or '',
                'spotifyLink': spotify_data['spotifyLink'] if spotify_data else '',
                'previewUrl': spotify_data.get('previewUrl', '')
            }
            songs_with_links.append(song_info)
        
        recommendations['songs'] = songs_with_links
        return recommendations
    except Exception as e:
        return {"error": str(e), "details": str(e)}

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully","user_id": new_user.id}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return jsonify({"message": "Login successful", "user_id": user.id}), 200
    
    return jsonify({"error": "Invalid credentials"}), 401
@app.route('/api/recommendations', methods=['POST'])
def recommendations():
    data = request.json
    mood = data.get('mood')
    client_hour = data.get('hour')
    user_id = data.get('user_id')

    if not mood or client_hour is None or not user_id:
        return jsonify({"error": "Mood, hour, and user_id are required"}), 400
 
    
    try:
        # Verify user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        recommendations = get_recommendations(model, mood, client_hour)
        
        mood_record = MoodRecord(
            user_id=user_id, 
            mood=mood, 
            cuisine=recommendations.get('cuisine', ''),
            explanation=recommendations.get('explanation', '')
        )
        db.session.add(mood_record)
        db.session.flush()

        songs_to_add = [
            Song(
                mood_record_id=mood_record.id, 
                title=song.get('title', ''),
                youtube_link=song.get('youtubeLink', ''),
                spotify_link=song.get('spotifyLink', '')
            ) for song in recommendations.get('songs', [])
        ]
        db.session.add_all(songs_to_add)
        
        db.session.commit()

        return jsonify(recommendations)

    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error: {str(e)}")
        return jsonify({"error": "Database error occurred"}), 500

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True, port=5000)