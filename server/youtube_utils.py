import os
import requests
from dotenv import load_dotenv

load_dotenv()

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
