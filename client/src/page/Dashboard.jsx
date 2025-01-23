import React, { useState, useEffect } from 'react';
import { Music, Info, Coffee } from 'lucide-react';
import { AiOutlineSpotify } from "react-icons/ai";
import { FiYoutube } from "react-icons/fi";
import { Button } from "@material-tailwind/react";
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const [mood, setMood] = useState('');
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [user_id, setUserId] = useState(null);
  const navigate = useNavigate(); 
  // Initialize user_id from localStorage
  useEffect(() => {
    const storedUserId = localStorage.getItem('userId');
    if (storedUserId) {
      setUserId(storedUserId);
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    const currentHour = new Date().getHours();

    try {
      const response = await fetch(`${import.meta.env.VITE_SERVER_API}/api/recommendations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ mood, hour: currentHour, user_id }),
      });

      if (!response.ok) {
        throw new Error('Failed to get recommendations');
      }

      const data = await response.json();
      console.log('API Response:', data);

      // Ensure the data is in the correct format
      if (!data.songs || !Array.isArray(data.songs)) {
        throw new Error('Invalid response format');
      }
      setRecommendations(data);
    } catch (err) {
      setError('Failed to get recommendations. Please try again.');
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handlelogout = ()=>{
    
    localStorage.clear();
    navigate('/');
      
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 to-blue-100 p-8">
      <div className="max-w-2xl mx-auto">
        <div className="text-center mb-12">
          <div className="flex justify-center items-center mb-4">
            <div className="bg-white p-4 rounded-full shadow-lg">
              <Music size={40} className="text-purple-600" />
            </div>
          </div>
          <h1 className="text-4xl font-bold text-gray-800 mb-2">Mood Harmony</h1>
          <p className="text-gray-600">Get personalized food and music recommendations based on your mood</p>
        </div>

        <form onSubmit={handleSubmit} className="mb-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <input
              type="text"
              value={mood}
              onChange={(e) => setMood(e.target.value)}
              placeholder="How are you feeling right now?"
              className="w-full p-4 border border-gray-300 rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-purple-500"
              required
            />
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-purple-600 text-white py-3 rounded-lg hover:bg-purple-700 transition duration-200"
            >
              {loading ? 'Getting Recommendations...' : 'Get Recommendations'}
            </button>

            <div className='pt-2 italic font-light text-xs flex justify-end '>
            It may take some time since it's running on the Gemini free tier.
            </div>
          </div>
        </form>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {recommendations && (
          <div className="space-y-6">
            {/* Cuisine Recommendation */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center mb-4">
                <Coffee className="text-purple-600 mr-2" />
                <h2 className="text-xl font-semibold">Cuisine Recommendation</h2>
              </div>
              <p className="text-gray-700">{recommendations.cuisine}</p>
            </div>

            {/* Music Recommendations */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center mb-4">
                <Music className="text-purple-600 mr-2" />
                <h2 className="text-xl font-semibold">Music Recommendations</h2>
              </div>
              <div className="space-y-4">
                {recommendations.songs && recommendations.songs.length > 0 ? (
                  <ul className="space-y-3">
                    {recommendations.songs.map((song, index) => (
                      <li key={index} className="bg-gray-50 p-3 rounded-lg flex justify-between items-center">
                        <span className="text-gray-800">{song.title}</span>
                        <div className="flex space-x-2">
                          {song.youtubeLink && (
                            <a 
                              href={song.youtubeLink} 
                              target="_blank" 
                              rel="noopener noreferrer"
                              className="text-red-600 hover:text-red-700 transition-colors"
                            >
                              <FiYoutube size={24} />
                            </a>
                          )}
                          {song.spotifyLink && (
                            <a 
                              href={song.spotifyLink} 
                              target="_blank" 
                              rel="noopener noreferrer"
                              className="text-green-600 hover:text-green-700 transition-colors"
                            >
                              {/* <Spotify size={24} /> */}
                              <AiOutlineSpotify size={24}/>
                            </a>
                          )}
                        </div>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-gray-500">No songs available at the moment.</p>
                )}
              </div>
            </div>

            {/* Explanation */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center mb-4">
                <Info className="text-purple-600 mr-2" />
                <h2 className="text-xl font-semibold">Why These Recommendations?</h2>
              </div>
              <p className="text-gray-700">{recommendations.explanation}</p>
            </div>
          </div>
        )}
      </div>
      <div className='flex justify-center'>
        <div className='bg-slate-500'>
          <button onClick={handlelogout} className='w-full bg-red-600 p-4 text-white py-3 rounded-xl'>Logout</button>
      </div>
      </div>
    </div>
  );
};

export default Dashboard;