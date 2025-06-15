// App.jsx
import React, { useState } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Signup from "./components/Signup";
import Login from "./components/Login";
import ChatPage from "./components/ChatPage";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token"));

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  return (
    <Routes>
      {}
      <Route
        path="/"
        element={
          token ? (
            <ChatPage token={token} onLogout={handleLogout} />
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />
      {/* Public routes */}
      <Route path="/login" element={<Login setToken={setToken} />} />
      <Route path="/signup" element={<Signup />} />
    </Routes>
  );
}

export default App;
