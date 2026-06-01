# Software Requirements Specification (SRS)
## AI-Powered Quiz Generator from Lecture Notes

---

**Project Title:** AI-Powered Quiz Generator from Lecture Notes  
**Course:** CEC418 — Software Construction and Evolution  
**Institution:** University of Buea, College of Technology, Department of Computer Engineering  
**Academic Year:** 2025/2026  
**Student:** Chasieh Hopkins Bah Yengho  
**Matricule:** CT25A434  
**Date:** May 2026  

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [Functional Requirements](#3-functional-requirements)
4. [Non-Functional Requirements](#4-non-functional-requirements)
5. [System Architecture Overview](#5-system-architecture-overview)
6. [External Interface Requirements](#6-external-interface-requirements)
7. [Constraints and Assumptions](#7-constraints-and-assumptions)
8. [Use Cases](#8-use-cases)

---

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) defines the functional and non-functional requirements for the AI-Powered Quiz Generator — a web-based platform that accepts lecture notes from educators and students and automatically generates structured quizzes using Natural Language Processing (NLP) via the Groq API.

### 1.2 Scope
The system, referred to as **QuizGen**, will:
- Accept lecture notes in plain text or PDF format
- Use the Groq API to generate multiple-choice, true/false, and short-answer questions
- Provide an interactive quiz-taking interface with scoring and feedback
- Allow educators to save and share quizzes with students
- Be deployed using Docker containers on Render, with CircleCI managing the CI/CD pipeline

The system will be accessible via modern web browsers on desktop and mobile devices. Native mobile applications, LMS integrations (Moodle, Blackboard), and custom AI model training are explicitly out of scope.

### 1.3 Definitions and Acronyms

| Term | Definition |
|------|-----------|
| SRS | Software Requirements Specification |
| NLP | Natural Language Processing |
| LLM | Large Language Model |
| API | Application Programming Interface |
| JWT | JSON Web Token |
| CI/CD | Continuous Integration / Continuous Deployment |
| UAT | User Acceptance Testing |
| PDF | Portable Document Format |
| ORM | Object-Relational Mapping |
| SPA | Single Page Application |

### 1.4 References
- SWEBOK Software Construction Knowledge Area (Unit 1 — CEC418)
- Groq API Documentation
- Flask Documentation (https://flask.palletsprojects.com)
- Docker Documentation (https://docs.docker.com)
- CircleCI Documentation (https://circleci.com/docs)

---

## 2. Overall Description

### 2.1 Product Perspective
QuizGen is a standalone web application. It interfaces with:
- The **Groq API** for AI-powered question generation
- A **PostgreSQL** database for persistent data storage
- **Render** as the cloud hosting platform
- **CircleCI** for automated testing and deployment

### 2.2 Product Functions (Summary)
- User registration and authentication (students and lecturers)
- Lecture note upload (text and PDF)
- AI-powered quiz generation via Groq API
- Interactive quiz-taking with real-time scoring
- Quiz management dashboard (save, retake, share)
- Educator dashboard for managing and distributing quizzes

### 2.3 User Classes

| User Class | Description | Access Level |
|------------|-------------|--------------|
| Student | Uploads notes, takes quizzes, views results | Standard |
| Lecturer | Uploads notes, generates, manages, and shares quizzes | Elevated |
| Admin | Manages user accounts and system settings | Full |

### 2.4 Operating Environment
- **Client:** Any modern browser (Chrome, Firefox, Edge, Safari) on desktop or mobile
- **Server:** Python 3.11, Flask, running inside a Docker container on Render
- **Database:** PostgreSQL (production), SQLite (local development)
- **OS:** Linux (Ubuntu) inside Docker containers

### 2.5 Design and Implementation Constraints
- The system must use the Groq API for question generation (no custom model training)
- PDF uploads are limited to 10MB
- The backend must be built with Flask (Python)
- All services must be containerized using Docker
- CI/CD pipeline must be implemented using CircleCI

---

## 3. Functional Requirements

### 3.1 User Authentication

| ID | Requirement |
|----|-------------|
| FR-01 | The system shall allow users to register with an email, password, and role (student or lecturer) |
| FR-02 | The system shall authenticate users via email and password and issue a JWT token |
| FR-03 | The system shall protect all dashboard and quiz routes from unauthenticated access |
| FR-04 | The system shall allow users to log out, invalidating their session token |

### 3.2 Lecture Note Upload

| ID | Requirement |
|----|-------------|
| FR-05 | The system shall accept lecture notes as plain text input via a text area |
| FR-06 | The system shall accept PDF file uploads up to 10MB in size |
| FR-07 | The system shall extract text from uploaded PDFs using PyMuPDF |
| FR-08 | The system shall reject unsupported file types with a clear error message |

### 3.3 Quiz Generation

| ID | Requirement |
|----|-------------|
| FR-09 | The system shall send extracted lecture note text to the Groq API with a structured prompt |
| FR-10 | The system shall generate multiple-choice questions (4 options, 1 correct answer) |
| FR-11 | The system shall generate true/false questions |
| FR-12 | The system shall generate short-answer questions |
| FR-13 | The system shall allow users to specify the number of questions to generate (5–20) |
| FR-14 | The system shall parse the Groq API JSON response and store questions in the database |
| FR-15 | The system shall display a loading indicator during quiz generation |

### 3.4 Quiz Taking

| ID | Requirement |
|----|-------------|
| FR-16 | The system shall present generated questions one at a time in an interactive card interface |
| FR-17 | The system shall include an optional countdown timer for quiz sessions |
| FR-18 | The system shall calculate and display the user's score upon quiz completion |
| FR-19 | The system shall display correct answers and explanations after submission |
| FR-20 | The system shall record each quiz attempt in the database linked to the user |

### 3.5 Quiz Management

| ID | Requirement |
|----|-------------|
| FR-21 | The system shall allow users to save generated quizzes to their dashboard |
| FR-22 | The system shall allow users to retake previously saved quizzes |
| FR-23 | The system shall allow lecturers to share a quiz via a unique link |
| FR-24 | The system shall display a history of all quiz attempts with scores and dates |

---

## 4. Non-Functional Requirements

### 4.1 Performance

| ID | Requirement |
|----|-------------|
| NFR-01 | Quiz generation shall complete within 15 seconds under normal network conditions |
| NFR-02 | Page load time shall not exceed 3 seconds on a standard broadband connection |
| NFR-03 | The system shall support at least 50 concurrent users without performance degradation |

### 4.2 Security

| ID | Requirement |
|----|-------------|
| NFR-04 | All user passwords shall be hashed using bcrypt before storage |
| NFR-05 | All API communication shall use HTTPS |
| NFR-06 | JWT tokens shall expire after 24 hours |
| NFR-07 | The Groq API key shall never be exposed to the client side |
| NFR-08 | Input text shall be sanitized before being sent to the AI API |

### 4.3 Usability

| ID | Requirement |
|----|-------------|
| NFR-09 | The interface shall be fully responsive on screens from 320px to 1920px width |
| NFR-10 | Error messages shall be clear, human-readable, and suggest corrective action |
| NFR-11 | The system shall provide visual feedback for all loading states |

### 4.4 Reliability

| ID | Requirement |
|----|-------------|
| NFR-12 | The system shall have an uptime of at least 99% during evaluation periods |
| NFR-13 | Failed quiz generation attempts shall not corrupt existing user data |
| NFR-14 | The system shall gracefully handle Groq API timeouts with a user-friendly error |

### 4.5 Maintainability

| ID | Requirement |
|----|-------------|
| NFR-15 | All backend code shall follow PEP 8 Python style guidelines |
| NFR-16 | All functions shall include docstrings describing purpose, parameters, and return values |
| NFR-17 | The codebase shall maintain a minimum test coverage of 70% on critical backend routes |

---

## 5. System Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                    CLIENT BROWSER                    │
│         HTML + Tailwind CSS + JavaScript             │
└────────────────────────┬────────────────────────────┘
                         │ HTTP/HTTPS
┌────────────────────────▼────────────────────────────┐
│               FLASK BACKEND (Docker)                 │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────┐ │
│  │  Auth    │  │  Quiz    │  │   AI Service       │ │
│  │  Routes  │  │  Routes  │  │ (Groq API calls) │ │
│  └──────────┘  └──────────┘  └────────────────────┘ │
│                      │                               │
│              ┌───────▼──────┐                        │
│              │  SQLAlchemy  │                        │
│              │     ORM      │                        │
└──────────────┴───────┬──────┴────────────────────────┘
                       │
         ┌─────────────▼──────────────┐
         │     PostgreSQL Database     │
         │  Users | Quizzes | Attempts │
         └────────────────────────────┘
                       
         ┌─────────────────────────────┐
         │        Groq API             │
         │  (LLaMA — External)         │
         └─────────────────────────────┘
```

---

## 6. External Interface Requirements

### 6.1 User Interface
- The frontend will be built as a Single Page Application using HTML, Tailwind CSS, and Vanilla JavaScript
- Key screens: Landing page, Register/Login, Note Upload, Quiz Generation, Quiz Taking, Results, Dashboard

### 6.2 Groq API Interface
- **Endpoint:** `console.groq.com`
- **Model:** `LLaMA 3.3 70B`
- **Input:** Structured prompt containing lecture note text and question type/count instructions
- **Output:** JSON-formatted list of questions, options, correct answers, and explanations
- **Authentication:** API key stored as environment variable (`GROQ_API_KEY`)

### 6.3 Database Interface
- SQLAlchemy ORM used for all database interactions
- PostgreSQL in production (via Docker container)
- SQLite for local development (no Docker required)

### 6.4 DevOps Interfaces
- **GitHub:** Source code hosted at `https://github.com/Lebs-Anonymous05/quiz_gen`
- **CircleCI:** Connected to GitHub repo; triggers on push to `develop`, deploys on merge to `main`
- **Render:** Hosts the Flask backend and serves the frontend via Nginx
- **Docker Hub:** Stores built Docker images pushed by CircleCI

---

## 7. Constraints and Assumptions

### 7.1 Constraints
- The system relies on the Groq API; extended API downtime will affect quiz generation
- Free-tier hosting on Render may cause cold starts (first request after inactivity may be slow)
- PDF text extraction quality depends on whether the PDF contains selectable text (scanned image PDFs will not extract correctly)

### 7.2 Assumptions
- Users have a stable internet connection
- Uploaded lecture notes are in English
- Lecturers and students have access to a modern web browser
- The Groq API will remain available throughout the project evaluation period

---

## 8. Use Cases

### UC-01: Generate a Quiz from Lecture Notes

| Field | Detail |
|-------|--------|
| **Actor** | Student or Lecturer |
| **Precondition** | User is logged in |
| **Main Flow** | 1. User navigates to the Upload page. 2. User uploads a PDF or pastes text. 3. User selects question types and count. 4. System sends content to Groq API. 5. Groq API returns structured questions. 6. System displays quiz to user. |
| **Alternative Flow** | If Groq API times out, system displays an error and prompts the user to retry. |
| **Postcondition** | Quiz is displayed and optionally saved to user dashboard. |

### UC-02: Take a Quiz

| Field | Detail |
|-------|--------|
| **Actor** | Student |
| **Precondition** | A quiz has been generated or shared |
| **Main Flow** | 1. User opens a quiz. 2. System presents questions one by one. 3. User selects/enters answers. 4. User submits the quiz. 5. System calculates score and displays results with correct answers. |
| **Postcondition** | Attempt is recorded in the database with the user's score. |

### UC-03: Share a Quiz

| Field | Detail |
|-------|--------|
| **Actor** | Lecturer |
| **Precondition** | Lecturer has a saved quiz |
| **Main Flow** | 1. Lecturer opens their dashboard. 2. Lecturer clicks "Share" on a quiz. 3. System generates a unique shareable link. 4. Lecturer copies and distributes the link to students. |
| **Postcondition** | Students can access the quiz via the link without needing to generate it themselves. |

---

*Document Version: 1.0 — Initial Release*  
*Next Review: After System Design Phase*
