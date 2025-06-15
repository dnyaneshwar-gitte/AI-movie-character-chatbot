// ChatPage.jsx
import React, { useState, useRef, useEffect } from "react";
import "./ChatPage.css";

const ChatPage = ({ token, onLogout }) => {
  const [character, setCharacter] = useState("");
  const [message, setMessage] = useState("");
  const [chatLog, setChatLog] = useState([]);
  const chatLogRef = useRef(null);

  const sendMessage = async () => {
    if (!character.trim() || !message.trim()) return;

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ character, user_message: message }),
      });
      const data = await res.json();

      setChatLog((prev) => [
        ...prev,
        { from: "user", text: message.trim() },
        { from: "bot", text: data.response },
      ]);

      setMessage("");
    } catch (err) {
      alert("Failed to send message. Please login again.");
      onLogout();
    }
  };

  useEffect(() => {
    if (chatLogRef.current) {
      chatLogRef.current.scrollTop = chatLogRef.current.scrollHeight;
    }
  }, [chatLog]);

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleNewChat = () => {
    setCharacter("");
    setMessage("");
    setChatLog([]);
  };

  return (
    <div className="page-with-sidebar">
      <aside className="sidebar">
        <h2>Menu</h2>
        <ul>
          <li><button onClick={handleNewChat}>New Chat</button></li>
          <li><button>About Us</button></li>
          <li><button>Movie Available</button></li>
          <li><button>Settings</button></li>
        </ul>
      </aside>

      <div className="chat-container">
        <button className="logout-btn" onClick={onLogout}>Logout</button>
        <h1 className="title">🎬 Chat with a Movie Character</h1>

        <div className="input-group">
          <input
            type="text"
            className="input character"
            placeholder="Character"
            value={character}
            onChange={(e) => setCharacter(e.target.value)}
            spellCheck={false}
            autoComplete="off"
          />
          <input
            type="text"
            className="input message"
            placeholder="Your message"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            spellCheck={true}
            autoComplete="off"
          />
          <button className="send-btn" onClick={sendMessage}>Send</button>
        </div>

        <div className="chat-log" ref={chatLogRef}>
          {chatLog.map((chat, idx) => (
            <div
              key={idx}
              className={`message ${chat.from === "user" ? "user" : "bot"}`}
              title={chat.from === "user" ? "You" : "Character"}
            >
              {chat.text}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
