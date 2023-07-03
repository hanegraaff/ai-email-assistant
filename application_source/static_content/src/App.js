import React, { useState, useEffect } from 'react';
import './App.css';

const App = () => {
  const [result, setResult] = useState('');
  const [banner, setBanner] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const callApi = async () => {
    const response = await fetch('https://api-prod.hal-9001.com/test-data');
    const data = await response.json();
    setResult(JSON.stringify(data, null, 2));
  }

  useEffect(() => {
    const messages = ["Beware", "Go Away", "You shouldn't be here", "System Failure", "Don't do this", "It's all your fault", "You will regret it"];
    const bannerMessage = messages[Math.floor(Math.random() * messages.length)];
    setBanner(bannerMessage);
  }, []);

  return (
    <div className="container">
      <div className="banner" onClick={callApi}>{banner}</div>
      
      <input
        className="input"
        placeholder="Username"
        style={{color: 'rgba(120, 0, 0, 1)'}}
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      
      <input
        className="input"
        placeholder="Password"
        style={{color: 'rgba(120, 0, 0, 1)'}}
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <div className="googleLogin">
        <a className="link" href="https://accounts.google.com/o/oauth2/v2/auth?client_id=CLIENT_ID&redirect_uri=https://localhost:80&response_type=code&scope=https://www.googleapis.com/auth/userinfo.profile&access_type=offline&prompt=consent">
          Google Login
        </a>
      </div>

      <div className="results">{result}</div>
    </div>
  );
}

export default App;
