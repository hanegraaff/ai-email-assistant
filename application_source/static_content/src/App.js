import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './pages/Home';
import LoginPage from './pages/Login';

const App = () => {
  return (
    <Router>
      <div>
        <Routes>
          <Route exact path="/" element={<LoginPage />} />
          <Route path="/home" element={<HomePage />} />
          {/* Add more routes for additional pages */}
        </Routes>
      </div>
    </Router>
  );
};

export default App;
