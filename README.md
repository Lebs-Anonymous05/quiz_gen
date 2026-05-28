# QuizGen — AI-Powered Quiz Generator from Lecture Notes

## Project Description
A web-based platform that accepts lecture notes and generates AI-powered quizzes using NLP. Built with Flask, PostgreSQL, and integrated with Groq API (LLaMA 3.3 70B).

## Live Demo
🌐 **https://quizgen.up.railway.app**

## Tech Stack
- **Frontend:** HTML, Tailwind CSS, JavaScript
- **Backend:** Python 3.11, Flask, SQLAlchemy, PyMuPDF
- **Database:** PostgreSQL (production), SQLite (development)
- **AI/ML:** Groq API (LLaMA 3.3 70B) — NLP question generation
- **DevOps:** GitHub, Docker, CircleCI, Railway

## Progress Log

### ✅ Step 1 — Requirements Analysis (Done)
- Stakeholder needs identified
- Functional and non-functional requirements defined
- SRS document produced

### ✅ Step 2 — System Design (Done)
- 3-tier architecture designed
- Database schema defined
- API endpoints designed
- DevOps pipeline planned

### ✅ Step 3 — Frontend Development (Done)
- 6 pages built: Landing, Login, Dashboard, Upload, Quiz, Results
- Admin dashboard added
- Tailwind CSS styling throughout
- Auth guard and JWT token handling on all protected pages
- Mobile responsive with horizontal scroll on tables

### ✅ Step 4 — Backend Development (Done)
- Flask app running with Blueprints
- JWT authentication (register, login, logout)
- Quiz generation with Groq AI (LLaMA 3.3 70B)
- PDF upload and text extraction via PyMuPDF
- Quiz CRUD endpoints
- Attempt submission and history
- Admin routes (stats, users, quizzes, role management)
- Share quiz via unique link

### ✅ Step 5 — DevOps Setup (Done)
- GitHub version control with main/develop branches
- Docker containerization
- Procfile for Railway deployment

### ✅ Step 6 — AI Integration (Done)
- Groq API integrated (LLaMA 3.3 70B model)
- Quiz generation working end to end
- PDF text extraction ready via PyMuPDF
- Text truncation to stay within token limits
- Mock fallback available for offline testing

### ✅ Step 7 — Testing (Done)
- 8/8 pytest tests passing
- Auth tests: register, duplicate email, login, wrong password
- Quiz tests: generate, get all, get by id, delete
- In-memory SQLite used for test isolation
- CircleCI pipeline running tests on every push

### ✅ Step 8 — Deployment (Done)
- Backend deployed to Railway
- PostgreSQL database provisioned on Railway
- Frontend served via Flask static files
- Docker containerization with frontend included
- CI/CD via CircleCI — tests run on every push
- Live URL: https://quizgen.up.railway.app

## Running Locally

### Prerequisites
- Python 3.11
- Groq API key from https://console.groq.com

### Setup
```bash
# Clone the repo
git clone https://github.com/Lebs-Anonymous05/quiz_gen
cd quiz_gen/backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your API keys to .env

# Run the app
python run.py
```

Open `http://127.0.0.1:5000` in your browser.

## Environment Variables
| Variable | Description |
|----------|-------------|
| `FLASK_ENV` | `development` or `production` |
| `SECRET_KEY` | Flask secret key |
| `JWT_SECRET_KEY` | JWT signing key |
| `GROQ_API_KEY` | Groq API key |
| `DATABASE_URL` | PostgreSQL connection string |
