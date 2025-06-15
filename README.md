# 🎬 AI Movie Character Chatbot

This is a full-stack application where users can chat with famous movie characters like **Joker**, **Iron Man**, etc., using real script dialogues. The chatbot combines **FastAPI**, **MongoDB**, **Pinecone**, **Groq**, and a **React frontend** to provide accurate and intelligent conversations.

---

## 📌 Features

- 🔐 JWT-based Signup & Login system
- 🎭 Chat with AI-powered movie characters
- 🧠 Embedding and vector similarity search using Pinecone
- 💬 Fallback to Groq/OpenAI if dialogue not found
- 🔁 Dialogue caching using Redis
- 🌐 Full React-based frontend UI
- ⚡ Rate limiting and response time optimization

---

## 🧰 Tech Stack

**Backend (Python + FastAPI)**
- FastAPI
- MongoDB Atlas
- Pinecone Vector DB
- Redis
- Groq/OpenAI (LLM API)
- Sentence Transformers
- BeautifulSoup (for script scraping)

**Frontend (React)**
- React.js
- Axios
- React Router
- Custom CSS

---

## 📦 How to Install and Run the Project

### 🔹 Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/ai-movie-chatbot.git
cd ai-movie-chatbot
```
⚙️ Backend Setup
🔸 Go to Backend Folder

        cd backend
        
🔸 Create Virtual Environment and Activate

    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    
🔸 Install Required Packages

    pip install -r requirements.txt

🔸 Create .env File (in backend/)

    MONGO_URI=your_mongodb_uri
    PINECONE_API_KEY=your_pinecone_api_key
    PINECONE_ENV=your_pinecone_environment
    GROQ_API_KEY=your_groq_or_openai_key
    JWT_SECRET=your_jwt_secret
    REDIS_URL=redis_URL

🔸 Run the Backend Server

    uvicorn main:app --reload
    Server runs at: http://localhost:8000
    Swagger docs: http://localhost:8000/docs

🎨 Frontend Setup
🔸 Go to Frontend Directory

    cd ../frontend/movie-chatbot-frontend
    
🔸 Install Frontend Dependencies

    npm install
    
🔸 Start the Frontend

    npm start
Frontend runs at: http://localhost:3000

css
Copy code
You wanna know how I got these scars?
📁 Folder Structure

    AI Movie/
    ├── movie-chatbot-frontend/ # React Frontend
    │ ├── src/
    │ │ ├── App.jsx
    │ │ ├── App.test.js
    │ │ ├── index.js
    │ │ ├── index.css
    │ │ ├── App.css
    │ │ ├── logo.svg
    │ │ ├── reportWebVitals.js
    │ │ └── setupTests.js
    │ ├── .gitignore
    │ ├── package.json
    │ ├── package-lock.json
    │ └── README.md
    │
    ├── auth_routes.py
    ├── auth.py
    ├── data_loader.py
    ├── database.py
    ├── history_routes.py
    ├── locustfile.py
    ├── main.py
    ├── pinecone_client.py
    ├── rate_limiter.py
    ├── redis_cache.py
    ├── services.py
    ├── requirements.txt
    └── README.md 
.gitignore Suggestions
Make sure this is in your .gitignore:

    __pycache__/
    *.pyc
    .env
    node_modules/
    build/
    dist/
    .vscode/
    .idea/


Pinecone and Groq/OpenAI for NLP capabilities

FastAPI and React community
