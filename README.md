# 🎬 AI Movie Character Chatbot

An intelligent chatbot that lets you **chat with movie characters** using real movie scripts. It uses **FastAPI**, **MongoDB**, **Pinecone**, **Groq/OpenAI**, and a clean **React frontend**.

> 💬 Ask: “Why so serious?” and get an answer like the real Joker.

---

## 🔧 Tech Stack

**Backend**
- FastAPI (Python)
- MongoDB (Atlas)
- Pinecone (Vector DB)
- Redis (Rate limiting, caching)
- Sentence Transformers
- Groq/OpenAI (LLM API)

**Frontend**
- React.js (with Router)
- Axios
- Responsive CSS

**Utilities**
- JWT Authentication
- dotenv for config
- Locust (Load testing)
- BeautifulSoup (script scraping)

---

## 📦 Installation Guide

### 1. 📥 Clone the Repository

```bash
git clone https://github.com/your-username/ai-movie-chatbot.git
cd ai-movie-chatbot
⚙️ Backend Setup (FastAPI)
2. 🔌 Create a virtual environment & install dependencies
bash
Copy code
cd backend
python -m venv venv
source venv/bin/activate  # Use venv\Scripts\activate on Windows
pip install -r requirements.txt
3. 🔐 Set up .env
Create a .env file inside backend/:

env
Copy code
MONGO_URI=your_mongo_connection_string
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENV=your_pinecone_env
GROQ_API_KEY=your_groq_or_openai_key
JWT_SECRET=your_jwt_secret
REDIS_URL=redis://localhost:6379
4. 🚀 Run the backend server
bash
Copy code
uvicorn main:app --reload
Visit: http://localhost:8000
API Docs: http://localhost:8000/docs

🎨 Frontend Setup (React)
5. 📁 Install frontend dependencies
bash
Copy code
cd ../frontend/movie-chatbot-frontend
npm install
6. 🧠 Start the frontend
bash
Copy code
npm start
Visit: http://localhost:3000

🧪 Sample Usage
🔐 1. Sign up/Login via React frontend
Create an account

Login to receive JWT token

🎭 2. Select a movie character
E.g., “Joker”, “Iron Man”, or “Batman”

💬 3. Ask a question
Input:

perl
Copy code
Why did you say 'I am Iron Man'?
Response:

css
Copy code
I had to own who I was. No more secrets. I am Iron Man.
🧠 How it works:
The question is embedded using Sentence Transformers

Searched in Pinecone index of scraped dialogues

If match found → relevant response

Else → fallback to Groq LLM response

Cached in Redis

📁 Folder Structure
css
Copy code
ai-movie-chatbot/
│
├── backend/
│   ├── main.py
│   ├── auth.py
│   ├── services.py
│   ├── data_loader.py
│   ├── database.py
│   ├── pinecone_client.py
│   ├── rate_limiter.py
│   └── ...
│
├── frontend/
│   └── movie-chatbot-frontend/
│       ├── src/
│       ├── public/
│       ├── package.json
│       └── ...
│
├── .gitignore
├── requirements.txt
└── README.md
❌ What Not to Upload (Already in .gitignore)
node_modules/

__pycache__/

.env

.vscode/, .idea/

*.log

