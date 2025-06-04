// app.js

const socket = new WebSocket("ws://localhost:8000/ws/chat");

const log = document.getElementById("log");
const characterInput = document.getElementById("character");
const messageInput = document.getElementById("message");

socket.onmessage = function (event) {
  const data = JSON.parse(event.data);
  appendMessage("Server", data.response || JSON.stringify(data, null, 2));
};

function sendMessage() {
  const character = characterInput.value.trim();
  const message = messageInput.value.trim();

  if (!character || !message) return;

  const payload = {
    character,
    user_message: message
  };

  appendMessage("You", message);
  socket.send(JSON.stringify(payload));
  messageInput.value = "";
}

function appendMessage(sender, text) {
  const timestamp = new Date().toLocaleTimeString();
  log.textContent += `[${timestamp}] ${sender}: ${text}\n`;
  log.scrollTop = log.scrollHeight;
}
