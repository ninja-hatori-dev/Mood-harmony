from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from datetime import datetime
import json
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app)

def setup_gemini():
    """Initialize the Gemini model with API key from environment variable."""
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
    return f"""As an expert in both culinary arts and music therapy, provide personalized recommendations for someone who is feeling {mood} during the {time_of_day} (current hour: {hour}:00).
Please suggest:
1. A specific type of cuisine or dish that would complement and support their current emotional state
2. A genre or style of music that would be appropriate for their mood and the time of day
3. A brief explanation of why these recommendations would be beneficial

Format the response as a JSON object with the following structure:
{{
  "cuisine": "specific food recommendation",
  "musicGenre": "specific music recommendation",
  "explanation": "brief explanation of the recommendations"
}}"""

def get_recommendations(model, mood, hour):
    """Get personalized recommendations using Gemini."""
    prompt = create_prompt(mood, hour)
    response = model.generate_content(prompt)
    
    try:
        content = response.text
        cleaned_content = content.strip().strip("```json").strip("```")
        recommendations = json.loads(cleaned_content)
        return recommendations
    except Exception as e:
        return {"error": str(e)}

model = setup_gemini()

@app.route('/api/recommendations', methods=['POST'])
def recommendations():
    data = request.json
    mood = data.get('mood')
    client_hour = data.get('hour')  # Get hour from client
    
    if not mood:
        return jsonify({"error": "Mood is required"}), 400
    
    if client_hour is None:
        return jsonify({"error": "Hour is required"}), 400
    
    recommendations = get_recommendations(model, mood, client_hour)
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
