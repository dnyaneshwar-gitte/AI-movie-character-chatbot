🎬 AI Movie Character Chatbot
An intelligent chatbot that lets users chat with movie characters! Built with FastAPI, MongoDB, Pinecone, Groq/OpenAI, and React. This project scrapes movie scripts, generates embeddings, and stores dialogue in vector DB for intelligent retrieval-based responses.

📌 Features
🔐 JWT-based authentication (Signup/Login)

💬 Chat with movie characters based on real dialogues

📚 Dialogue scraping from script websites

🧠 RAG-based response system using Pinecone + LLMs (Groq/OpenAI)

🧠 Semantic embeddings via Sentence Transformers

💾 MongoDB (Atlas) for storing dialogues and user chats

⚡ Redis caching for fast response

🌐 React frontend with clean UI

🧪 Locust for load testing

🏗️ Tech Stack
Layer	Tech
Frontend	React, Axios, React Router
Backend	FastAPI, Pydantic, Uvicorn
Auth	JWT, OAuth2, Passlib
Database	MongoDB (Motor + PyMongo)
Vector DB	Pinecone
Embeddings	Sentence Transformers
LLM	Groq (or OpenAI-compatible)
Cache	Redis
DevOps	dotenv, Locust, CORS middleware

🗂️ Project Structure
bash
Copy code
├── backend/
│   ├── main.py               # FastAPI app entry point
│   ├── auth.py               # Authentication logic
│   ├── services.py           # Business logic
│   ├── database.py           # MongoDB operations
│   ├── pinecone_client.py    # Pinecone connection + embedding
│   ├── data_loader.py        # Script scrapers + ingestion
│   ├── rate_limiter.py       # Redis-based rate limiting
│   └── ...
├── frontend/
│   └── movie-chatbot-frontend/
│       ├── src/
│       │   ├── components/
│       │   ├── ChatPage.js
│       │   ├── Signup.js
│       │   ├── Login.js
│       │   └── ...
│       ├── package.json
│       └── ...
├── .env
├── requirements.txt
└── README.md
🚀 Getting Started
⚙️ 1. Clone the Repository
bash
Copy code
git clone https://github.com/yourusername/ai-movie-chatbot.git
cd ai-movie-chatbot
🧠 2. Backend Setup (FastAPI)
⬇️ Install Dependencies
bash
Copy code
cd backend
pip install -r requirements.txt
🗝️ Set Environment Variables
Create a .env file in the backend directory:

env
Copy code
MONGO_URI=your_mongodb_connection_string
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENV=your_pinecone_environment
GROQ_API_KEY=your_groq_or_openai_key
JWT_SECRET=your_jwt_secret
REDIS_URL=redis://localhost:6379
▶️ Run the Server
bash
Copy code
uvicorn main:app --reload
Your backend will be live at: http://127.0.0.1:8000

🎨 3. Frontend Setup (React)
bash
Copy code
cd frontend/movie-chatbot-frontend
npm install
npm start
Frontend will be available at: http://localhost:3000

🧪 Example API Endpoints
Method	Endpoint	Description
POST	/auth/signup	Register new user
POST	/auth/login	Login and get JWT token
POST	/chat/character	Get movie character reply
GET	/history	Get chat history

📸 Screenshots
(Add images of your app here: Chat UI, Signup/Login, etc.)

📌 Tips
Use Postman to test API endpoints.

You can preload movie scripts using data_loader.scrape_all_dialogues().

Pinecone index must be created before adding embeddings.

🧠 Sample Dialogue Flow
User selects a movie character.

Question is embedded using Sentence Transformers.

Embedding is searched in Pinecone for top dialogues.

If no match found, fallback to Groq/OpenAI response.

Response is cached in Redis for fast future access.
