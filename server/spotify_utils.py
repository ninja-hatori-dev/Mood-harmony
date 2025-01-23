import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

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

def get_spotify_link(song_title, artist):
    try:
        results = spotify_client.search(q=f'track:{song_title} artist:{artist}', type='track', limit=1)
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
