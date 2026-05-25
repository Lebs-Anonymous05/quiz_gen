# quiz_gen
AI-Powered Quiz Generator from Lecture Notes

## Project Description
A web-based platform that accepts lecture notes and generates AI-powered quizzes using NLP. Built with Flask, PostgreSQL, and integrated with Claude/OpenAI/groq API.

## Tech Stack
- **Frontend:** HTML, Tailwind CSS, JavaScript
- **Backend:** Python 3.11, Flask, SQLAlchemy, PyMuPDF
- **Database:** PostgreSQL (production), SQLite (development)
- **AI/ML:** Claude API / OpenAI GPT-4
- **DevOps:** GitHub, Docker, CircleCI, Render

## Project Structure
quiz_gen/
├── frontend/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   ├── models/
│   │   └── services/
│   └── tests/
├── docs/
└── docker-compose.yml

## Progress Log
### ✅ Step 1 — GitHub Setup (Done)
- Repository created with main and develop branches
- Folder structure initialized
- DevOps tools: GitHub, Docker, CircleCI, Render

### 🔄 Step 2 — SRS Document
[View SRS Document](docs/SRS.md)

### ✅ Step 3 — System Design (Done)
- [View System Design](docs/SYSTEM_DESIGN.md)

### ✅ Step 4 — Backend Scaffold (Done)
- Flask app running on port 5000
- Database models: User, Quiz, Question, Attempt
- Auth, Quiz, and Attempt routes registered
- Registration endpoint tested and working

### ✅ Step 5 — Frontend Scaffold (Done)
- 6 pages built: Landing, Login, Dashboard, Upload, Quiz, Results
- Tailwind CSS styling throughout
- Auth guard and JWT token handling on all protected pages

### 🔄 Step 6 — Claude API Integration (In Progress)
