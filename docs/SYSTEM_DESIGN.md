# System Design Document
## AI-Powered Quiz Generator from Lecture Notes

---

**Project Title:** AI-Powered Quiz Generator from Lecture Notes  
**Course:** CEC418 — Software Construction and Evolution  
**Institution:** University of Buea, College of Technology, Department of Computer Engineering  
**Academic Year:** 2025/2026  
**Student:** Chasieh Hopkins Bah Yengho  
**Matricule:** CT25A434  
**Version:** 1.0 — Initial Release  

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Database Schema](#2-database-schema)
3. [API Endpoint Design](#3-api-endpoint-design)
4. [Groq API Integration Design](#4-groq-api-integration-design)
5. [DevOps Pipeline Design](#5-devops-pipeline-design)
6. [Folder Structure](#6-folder-structure)

---

## 1. Architecture Overview

QuizGen follows a **3-tier architecture**:

```
┌─────────────────────────────────────────────────────────┐
│                   PRESENTATION TIER                      │
│         HTML + Tailwind CSS + Vanilla JavaScript         │
│   Landing | Auth | Upload | Quiz | Results | Dashboard   │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP/HTTPS (REST API)
┌─────────────────────▼───────────────────────────────────┐
│                   APPLICATION TIER                       │
│              Flask (Python 3.11) — Docker                │
│  ┌───────────┐  ┌────────────┐  ┌─────────────────────┐ │
│  │   Auth    │  │    Quiz    │  │    AI Service        │ │
│  │  Module   │  │   Module   │  │  (Groq API calls)  │ │
│  └───────────┘  └────────────┘  └─────────────────────┘ │
│                        │                                 │
│               ┌────────▼───────┐                         │
│               │  SQLAlchemy    │                         │
│               │     ORM        │                         │
└───────────────┴────────┬───────┴─────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                     DATA TIER                            │
│                 PostgreSQL Database                      │
│        users | quizzes | questions | attempts            │
└─────────────────────────────────────────────────────────┘

              ┌──────────────────────────────┐
              │       EXTERNAL SERVICE        │
              │           Groq API            │
              │  https://console.groq.com     │
              └──────────────────────────────┘
```

### Component Responsibilities

| Component | Technology | Responsibility |
|-----------|-----------|----------------|
| Frontend | HTML, Tailwind CSS, JS | UI rendering, user interaction, API calls |
| Backend | Flask (Python 3.11) | Business logic, routing, auth, AI orchestration |
| ORM | SQLAlchemy | Database abstraction, model definitions |
| Database | PostgreSQL | Persistent data storage |
| AI Service | Groq API | Natural language question generation |
| Container | Docker | Environment consistency across dev and prod |
| CI/CD | CircleCI | Automated testing and deployment |
| Hosting | Render | Cloud deployment and serving |

---

## 2. Database Schema

### 2.1 Entity Relationship Overview

```
users ──────────< quizzes ──────────< questions
  │                  │
  └──────────────< attempts >────────┘
```

### 2.2 Table: `users`

Stores registered user accounts for both students and lecturers.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique user identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email address |
| password_hash | VARCHAR(255) | NOT NULL | bcrypt hashed password |
| role | VARCHAR(20) | NOT NULL, DEFAULT 'student' | 'student' or 'lecturer' |
| full_name | VARCHAR(100) | NOT NULL | User's full name |
| created_at | TIMESTAMP | DEFAULT NOW() | Account creation time |
| is_active | BOOLEAN | DEFAULT TRUE | Account active status |

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'student',
    full_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);
```

### 2.3 Table: `quizzes`

Stores each quiz generated from lecture notes.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique quiz identifier |
| user_id | INTEGER | FOREIGN KEY → users.id | Quiz creator |
| title | VARCHAR(255) | NOT NULL | Quiz title |
| source_text | TEXT | NOT NULL | Original lecture note text |
| question_count | INTEGER | NOT NULL | Number of questions generated |
| share_token | VARCHAR(64) | UNIQUE, NULLABLE | Token for shareable link |
| created_at | TIMESTAMP | DEFAULT NOW() | Quiz creation time |

```sql
CREATE TABLE quizzes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    source_text TEXT NOT NULL,
    question_count INTEGER NOT NULL,
    share_token VARCHAR(64) UNIQUE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 2.4 Table: `questions`

Stores individual questions belonging to a quiz.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique question identifier |
| quiz_id | INTEGER | FOREIGN KEY → quizzes.id | Parent quiz |
| question_type | VARCHAR(20) | NOT NULL | 'mcq', 'true_false', 'short_answer' |
| question_text | TEXT | NOT NULL | The question content |
| options | JSON | NULLABLE | MCQ options as JSON array |
| correct_answer | TEXT | NOT NULL | Correct answer |
| explanation | TEXT | NULLABLE | AI-generated explanation |
| order_index | INTEGER | NOT NULL | Display order in quiz |

```sql
CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
    question_type VARCHAR(20) NOT NULL,
    question_text TEXT NOT NULL,
    options JSON,
    correct_answer TEXT NOT NULL,
    explanation TEXT,
    order_index INTEGER NOT NULL
);
```

### 2.5 Table: `attempts`

Records each time a user takes a quiz.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique attempt identifier |
| user_id | INTEGER | FOREIGN KEY → users.id | User who attempted |
| quiz_id | INTEGER | FOREIGN KEY → quizzes.id | Quiz that was attempted |
| score | FLOAT | NOT NULL | Score as percentage (0.0 – 100.0) |
| answers | JSON | NOT NULL | User's answers as JSON |
| completed_at | TIMESTAMP | DEFAULT NOW() | Attempt completion time |
| time_taken | INTEGER | NULLABLE | Time taken in seconds |

```sql
CREATE TABLE attempts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    quiz_id INTEGER NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
    score FLOAT NOT NULL,
    answers JSON NOT NULL,
    completed_at TIMESTAMP DEFAULT NOW(),
    time_taken INTEGER
);
```

---

## 3. API Endpoint Design

### Base URL
- **Development:** `http://localhost:5000/api`
- **Production:** `https://quiz-gen.onrender.com/api`

### Authentication
All protected routes require a JWT token in the request header:
```
Authorization: Bearer <token>
```

---

### 3.1 Auth Endpoints

#### POST `/api/auth/register`
Register a new user account.

**Request Body:**
```json
{
  "full_name": "Hopkins Bah",
  "email": "hopkins@example.com",
  "password": "securepassword123",
  "role": "student"
}
```

**Response (201):**
```json
{
  "message": "Account created successfully",
  "user": {
    "id": 1,
    "email": "hopkins@example.com",
    "role": "student"
  }
}
```

---

#### POST `/api/auth/login`
Authenticate a user and return a JWT token.

**Request Body:**
```json
{
  "email": "hopkins@example.com",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "full_name": "Hopkins Bah",
    "role": "student"
  }
}
```

---

#### POST `/api/auth/logout`
Invalidate the current user session. 🔒 Protected

**Response (200):**
```json
{
  "message": "Logged out successfully"
}
```

---

### 3.2 Quiz Endpoints

#### POST `/api/quiz/generate`
Generate a new quiz from lecture notes. 🔒 Protected

**Request Body (multipart/form-data or JSON):**
```json
{
  "title": "Introduction to Operating Systems Quiz",
  "source_text": "An operating system is system software...",
  "question_count": 10,
  "question_types": ["mcq", "true_false"]
}
```

**Response (201):**
```json
{
  "quiz_id": 42,
  "title": "Introduction to Operating Systems Quiz",
  "questions": [
    {
      "id": 1,
      "type": "mcq",
      "question": "What is the primary role of an operating system?",
      "options": ["A. Manage hardware resources", "B. Browse the internet", "C. Write code", "D. Store files only"],
      "correct_answer": "A",
      "explanation": "An OS manages hardware and software resources..."
    }
  ]
}
```

---

#### POST `/api/quiz/upload`
Upload a PDF and extract text for quiz generation. 🔒 Protected

**Request:** `multipart/form-data` with file field `lecture_note`

**Response (200):**
```json
{
  "extracted_text": "Chapter 1: Introduction to...",
  "page_count": 5,
  "word_count": 1240
}
```

---

#### GET `/api/quiz/`
Get all quizzes created by the authenticated user. 🔒 Protected

**Response (200):**
```json
{
  "quizzes": [
    {
      "id": 42,
      "title": "Introduction to Operating Systems Quiz",
      "question_count": 10,
      "created_at": "2026-05-25T10:30:00Z"
    }
  ]
}
```

---

#### GET `/api/quiz/<quiz_id>`
Get a specific quiz with all its questions. 🔒 Protected

**Response (200):**
```json
{
  "id": 42,
  "title": "Introduction to Operating Systems Quiz",
  "questions": [ ... ]
}
```

---

#### DELETE `/api/quiz/<quiz_id>`
Delete a quiz. 🔒 Protected (owner only)

**Response (200):**
```json
{
  "message": "Quiz deleted successfully"
}
```

---

#### POST `/api/quiz/<quiz_id>/share`
Generate a shareable link token for a quiz. 🔒 Protected (lecturer only)

**Response (200):**
```json
{
  "share_url": "https://quiz-gen.onrender.com/shared/abc123xyz"
}
```

---

#### GET `/api/quiz/shared/<token>`
Access a shared quiz without authentication. 🌐 Public

**Response (200):**
```json
{
  "id": 42,
  "title": "Introduction to Operating Systems Quiz",
  "questions": [ ... ]
}
```

---

### 3.3 Attempt Endpoints

#### POST `/api/attempt/<quiz_id>`
Submit a completed quiz attempt. 🔒 Protected

**Request Body:**
```json
{
  "answers": {
    "1": "A",
    "2": "True",
    "3": "The kernel manages processes"
  },
  "time_taken": 240
}
```

**Response (201):**
```json
{
  "score": 80.0,
  "correct": 8,
  "total": 10,
  "results": [
    {
      "question_id": 1,
      "your_answer": "A",
      "correct_answer": "A",
      "is_correct": true,
      "explanation": "..."
    }
  ]
}
```

---

#### GET `/api/attempt/history`
Get all quiz attempts by the authenticated user. 🔒 Protected

**Response (200):**
```json
{
  "attempts": [
    {
      "attempt_id": 1,
      "quiz_title": "Introduction to Operating Systems Quiz",
      "score": 80.0,
      "completed_at": "2026-05-25T11:00:00Z"
    }
  ]
}
```

---

## 4. Groq API Integration Design

### 4.1 Prompt Structure

The AI Service module sends the following structured prompt to Groq:

```
You are a quiz generator. Given the lecture notes below, generate exactly {count} questions.

Return ONLY a valid JSON array. No explanation, no preamble.

Question types to generate: {types}

Format:
[
  {
    "type": "mcq",
    "question": "...",
    "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
    "correct_answer": "A",
    "explanation": "..."
  },
  {
    "type": "true_false",
    "question": "...",
    "options": ["True", "False"],
    "correct_answer": "True",
    "explanation": "..."
  },
  {
    "type": "short_answer",
    "question": "...",
    "options": null,
    "correct_answer": "...",
    "explanation": "..."
  }
]

Lecture Notes:
{lecture_text}
```

### 4.2 API Call Flow

```
User submits notes
      ↓
Flask route receives request
      ↓
ai_service.py builds prompt
      ↓
POST to api.anthropic.com/v1/messages
      ↓
Parse JSON response
      ↓
Save questions to database
      ↓
Return quiz to user
```

### 4.3 Error Handling

| Scenario | Handling |
|----------|----------|
| API timeout (>15s) | Return 504 with retry message |
| Invalid JSON from Groq | Retry once with stricter prompt |
| API key missing | Return 500, log error server-side |
| Rate limit exceeded | Return 429 with wait time message |

---

## 5. DevOps Pipeline Design

### 5.1 Pipeline Flow

```
Developer pushes to develop branch
            ↓
    CircleCI triggered
            ↓
    ┌───────────────────┐
    │  Install deps      │
    │  Run pytest        │
    │  Check coverage    │
    └───────┬───────────┘
            │ Tests pass
            ↓
    Build Docker image
            ↓
    Push to Docker Hub
            ↓
    Merge to main (PR)
            ↓
    Render auto-deploys
```

### 5.2 CircleCI Config Overview (`config.yml`)

```yaml
version: 2.1
jobs:
  test:
    docker:
      - image: cimg/python:3.11
    steps:
      - checkout
      - run: pip install -r backend/requirements.txt
      - run: pytest backend/tests/ --cov=backend/app

  build:
    steps:
      - run: docker build -t quiz-gen .
      - run: docker push hopkinsbah/quiz-gen:latest

workflows:
  main:
    jobs:
      - test
      - build:
          requires: [test]
          filters:
            branches:
              only: main
```

### 5.3 Docker Setup Overview

Two containers managed by `docker-compose.yml`:

| Container | Image | Port | Purpose |
|-----------|-------|------|---------|
| web | python:3.11 | 5000 | Flask backend |
| db | postgres:15 | 5432 | PostgreSQL database |

---

## 6. Folder Structure

```
quiz_gen/
├── frontend/
│   ├── index.html          ← Landing page
│   ├── login.html          ← Auth page
│   ├── dashboard.html      ← User dashboard
│   ├── upload.html         ← Note upload page
│   ├── quiz.html           ← Quiz taking page
│   ├── results.html        ← Results page
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── auth.js
│       ├── quiz.js
│       └── dashboard.js
│
├── backend/
│   ├── app/
│   │   ├── __init__.py     ← Flask app factory
│   │   ├── config.py       ← Configuration (dev/prod)
│   │   ├── models/
│   │   │   ├── user.py     ← User model
│   │   │   ├── quiz.py     ← Quiz + Question models
│   │   │   └── attempt.py  ← Attempt model
│   │   ├── routes/
│   │   │   ├── auth.py     ← /api/auth endpoints
│   │   │   ├── quiz.py     ← /api/quiz endpoints
│   │   │   └── attempt.py  ← /api/attempt endpoints
│   │   └── services/
│   │       ├── ai_service.py    ← Groq API integration
│   │       └── pdf_service.py   ← PDF text extraction
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_quiz.py
│   │   └── test_attempt.py
│   ├── requirements.txt
│   └── .env.example
│
├── docs/
│   ├── SRS.md
│   └── SYSTEM_DESIGN.md    ← This document
│
├── docker-compose.yml
├── Dockerfile
├── .circleci/
│   └── config.yml
└── README.md
```

---

*Document Version: 1.0 — Initial Release*  
*Next: Backend scaffold and database models*