// filepath: [App.jsx](http://_vscodecontentref_/4)
import React, { useState, useEffect } from 'react';

const App = ({ googleClientId }) => {
  const [user, setUser] = useState(null);
  const [message, setMessage] = useState('');
  // const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;

  useEffect(() => {
    window.handleCredentialResponse = handleCredentialResponse;

    const script = document.createElement('script');
    script.src = "https://accounts.google.com/gsi/client";
    script.async = true;
    script.onload = () => {
      if (window.google) {
        window.google.accounts.id.initialize({
          client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID, // Use the prop here
          callback: handleCredentialResponse,
        });
        window.google.accounts.id.renderButton(
          document.getElementById("googleSignInDiv"),
          { theme: "outline", size: "large" }
        );
      }
    };
    document.head.appendChild(script);

    return () => {
      delete window.handleCredentialResponse;
    };
  }, [import.meta.env.VITE_GOOGLE_CLIENT_ID]); // Add googleClientId to dependencies

  const handleGoogleSuccess = async (credentialResponse) => {
    try {
      setMessage('Authenticating with backend...');
      const response = await fetch('http://localhost:5000/api/auth/google', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token: credentialResponse.credential }),
      });

      const data = await response.json();

      if (response.ok) {
        setUser(data.user);
        setMessage(`Welcome, ${data.user.name}!`);
      } else {
        setMessage(`Error: ${data.error}`);
      }

    } catch (error) {
      console.error('Login error:', error);
      setMessage('An error occurred during login. Please try again.');
    }
  };

  const handleCredentialResponse = (response) => {
    handleGoogleSuccess(response);
  };

  const handleLogout = () => {
    if (window.google && window.google.accounts) {
      window.google.accounts.id.disableAutoSelect();
    }
    setUser(null);
    setMessage('You have been logged out.');
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <div className="bg-white p-8 rounded-xl shadow-lg w-full max-w-sm text-center">
        <h1 className="text-2xl font-bold mb-6 text-gray-800">My App</h1>

        {user ? (
          <div className="space-y-4">
            <p className="text-lg text-gray-700">Hello, {user.name}!</p>
            <p className="text-sm text-gray-500">{user.email}</p>
            <button
              onClick={handleLogout}
              className="w-full bg-red-500 text-white font-semibold py-2 px-4 rounded-lg shadow-md hover:bg-red-600 transition-colors"
            >
              Log out
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            <p className="text-gray-600">Please sign in to continue.</p>
            <div className="flex justify-center" id="googleSignInDiv"></div>
          </div>
        )}

        {message && (
          <p className={`mt-4 text-sm ${message.startsWith('Error') ? 'text-red-500' : 'text-green-600'}`}>
            {message}
          </p>
        )}
      </div>
    </div>
  );
};

export default App;