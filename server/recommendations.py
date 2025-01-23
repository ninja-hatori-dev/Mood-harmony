import os
import json
import google.generativeai as genai
from datetime import datetime
import requests
from spotify_utils import get_spotify_link
from youtube_utils import get_youtube_link
from dotenv import load_dotenv
import json
import re
load_dotenv()

def setup_gemini():
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    if not GOOGLE_API_KEY:
        raise ValueError("API key not found in environment variables.")
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-pro')
    return model

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
3. A brief explanation of why these recommendations are beneficial.

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
    print(f"Getting recommendations for mood: {mood} and hour: {hour}")
    
    prompt = create_prompt(mood, hour)
    response = model.generate_content(prompt)
    
    print(f"Model response: {response}")
    
    try:
        content = response.result.candidates[0].content.parts[0].text
        
        # Remove the code block markdown and extract the JSON
        content_cleaned = re.sub(r'```json\n|\n```', '', content).strip()
        
        print(f"Cleaned response: {content_cleaned}")
        
        # Parse the cleaned content as JSON
        recommendations = json.loads(content_cleaned)
        print(f"Recommendations: {recommendations}")
        
        # Add YouTube and Spotify links to songs
        songs_with_links = []
        for song in recommendations['songs']:
            title_parts = song['title'].split(' - ')
            song_title = title_parts[0]
            artist = title_parts[1] if len(title_parts) > 1 else ''
            
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
        print(f"Error: {e}")
        return {"error": str(e), "details": str(e)}