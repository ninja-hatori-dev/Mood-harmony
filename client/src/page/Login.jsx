import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';



const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
  
    const handleLogin = async (e) => {
      e.preventDefault();
      try {
        const response = await fetch(`${import.meta.env.VITE_SERVER_API}/api/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
  
        const data = await response.json();
        if (response.ok) {
          // Store user ID in localStorage or context
          localStorage.setItem('userId', data.user_id);
          navigate('/dashboard');
        } else {
          // Handle login error
          alert(data.error);
        }
      } catch (error) {
        console.error('Login error:', error);
      }
    };
  
    return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-purple-200 to-blue-200">
          <div className="bg-white shadow-lg rounded-lg w-96 p-6">
            <h1 className="text-2xl font-bold text-center text-gray-800 mb-6">Register Here</h1>
            <form onSubmit={handleLogin} className="space-y-4">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-600">
                  Email
                </label>
                <input
                  type="email"
                  id="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your email"
                  className="w-full mt-1 px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
                  required
                />
              </div>
              <div>
                <label htmlFor="password" className="block text-sm font-medium text-gray-600">
                  Password
                </label>
                <input
                  type="password"
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  className="w-full mt-1 px-4 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
                  required
                />
              </div>
              <button
                type="submit"
                className="w-full bg-purple-600 text-white py-2 rounded-lg hover:bg-purple-700 transition duration-200 font-semibold"
              >
                Register
              </button>
            </form>
          
          </div>
        </div>
      );
    };

  export default Login;