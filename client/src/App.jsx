import React, { useState } from 'react';
import { Music, Coffee, Info } from 'lucide-react';

const App = () => {
  const [mood, setMood] = useState('');
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
console.log(import.meta.env.VITE_SERVER_API);
    try {
      const response = await fetch(`${import.meta.env.VITE_SERVER_API}/api/recommendations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ mood }),
      });

      if (!response.ok) {
        throw new Error('Failed to get recommendations');
      }

      const data = await response.json();
      setRecommendations(data);
    } catch (err) {
      setError('Failed to get recommendations. Please try again.');
    } finally {
      setLoading(false);
    }
  };

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
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center mb-4">
                <Coffee className="text-purple-600 mr-2" />
                <h2 className="text-xl font-semibold">Cuisine Recommendation</h2>
              </div>
              <p className="text-gray-700">{recommendations.cuisine}</p>
            </div>

            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center mb-4">
                <Music className="text-purple-600 mr-2" />
                <h2 className="text-xl font-semibold">Music Recommendation</h2>
              </div>
              <p className="text-gray-700">{recommendations.musicGenre}</p>
            </div>

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
    </div>
  );
};

export default App;