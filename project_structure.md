# InterPrep-AI Next Generation: Project Structure

## Overview

InterPrep-AI Next Generation is a comprehensive interview preparation platform that combines AI-powered question generation, company-specific practice, personalized learning paths, and a professional user interface. This document outlines the project structure and architecture.

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: React with Material UI
- **Database**: PostgreSQL
- **AI Integration**: Gemini API, SentenceTransformers, FAISS

## Project Structure

```
interprep-ai-nextgen/
├── backend/                      # Flask backend
│   ├── app/
│   │   ├── __init__.py           # Flask app initialization
│   │   ├── config.py             # Configuration settings
│   │   ├── extensions.py         # Flask extensions (SQLAlchemy, etc.)
│   │   ├── models/               # Database models
│   │   │   ├── __init__.py
│   │   │   ├── user.py           # User and profile models
│   │   │   ├── question.py       # Question and submission models
│   │   │   ├── learning.py       # Learning resources models
│   │   │   └── favorites.py      # User favorites and history
│   │   ├── api/                  # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py           # Authentication endpoints
│   │   │   ├── questions.py      # Question endpoints
│   │   │   ├── submissions.py    # Code submission endpoints
│   │   │   ├── learning.py       # Learning resources endpoints
│   │   │   └── users.py          # User management endpoints
│   │   ├── services/             # Business logic services
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py   # Authentication logic
│   │   │   ├── question_service.py # Question generation/retrieval
│   │   │   ├── evaluation_service.py # Code evaluation
│   │   │   └── learning_service.py # Learning content management
│   │   ├── ai/                   # AI integration
│   │   │   ├── __init__.py
│   │   │   ├── gemini.py         # Gemini API integration
│   │   │   ├── embeddings.py     # SentenceTransformer integration
│   │   │   └── search.py         # FAISS search integration
│   │   └── utils/                # Utility functions
│   │       ├── __init__.py
│   │       ├── security.py       # Security utilities
│   │       └── helpers.py        # Helper functions
│   ├── migrations/               # Database migrations
│   ├── tests/                    # Backend tests
│   ├── requirements.txt          # Python dependencies
│   └── run.py                    # Application entry point
│
├── frontend/                     # React frontend
│   ├── public/                   # Static files
│   ├── src/
│   │   ├── components/           # Reusable UI components
│   │   │   ├── common/           # Common UI elements
│   │   │   ├── auth/             # Authentication components
│   │   │   ├── dashboard/        # Dashboard components
│   │   │   ├── practice/         # Practice interface components
│   │   │   ├── learning/         # Learning resources components
│   │   │   └── profile/          # User profile components
│   │   ├── pages/                # Page components
│   │   │   ├── Home.jsx          # Landing page
│   │   │   ├── Login.jsx         # Login page
│   │   │   ├── Register.jsx      # Registration page
│   │   │   ├── Dashboard.jsx     # User dashboard
│   │   │   ├── Practice.jsx      # Practice interface
│   │   │   ├── Learning.jsx      # Learning resources
│   │   │   └── Profile.jsx       # User profile
│   │   ├── services/             # API client services
│   │   │   ├── api.js            # API client setup
│   │   │   ├── auth.js           # Authentication service
│   │   │   ├── questions.js      # Questions service
│   │   │   └── learning.js       # Learning resources service
│   │   ├── context/              # React context providers
│   │   │   ├── AuthContext.jsx   # Authentication context
│   │   │   └── UserContext.jsx   # User data context
│   │   ├── utils/                # Utility functions
│   │   ├── App.jsx               # Main application component
│   │   ├── index.jsx             # Entry point
│   │   └── theme.js              # Material UI theme
│   ├── package.json              # Node.js dependencies
│   └── README.md                 # Frontend documentation
│
└── README.md                     # Project documentation
```

## Database Schema

### User Management

```
users
├── id (PK)
├── username
├── email
├── password_hash
├── created_at
├── last_login
└── is_active

user_profiles
├── id (PK)
├── user_id (FK -> users.id)
├── full_name
├── bio
├── preferences (JSON)
└── settings (JSON)
```

### Questions and Submissions

```
questions
├── id (PK)
├── title
├── content
├── difficulty
├── topic
├── company
├── source_type (generated/book/user)
├── created_at
└── embedding (vector)

submissions
├── id (PK)
├── user_id (FK -> users.id)
├── question_id (FK -> questions.id)
├── code
├── language
├── status
├── feedback
└── submitted_at

favorites
├── id (PK)
├── user_id (FK -> users.id)
├── question_id (FK -> questions.id)
└── added_at

practice_history
├── id (PK)
├── user_id (FK -> users.id)
├── question_id (FK -> questions.id)
├── viewed_at
└── completed (boolean)
```

### Learning Resources

```
learning_categories
├── id (PK)
├── name
├── description
└── order

learning_topics
├── id (PK)
├── category_id (FK -> learning_categories.id)
├── name
├── description
├── order
└── icon

learning_content
├── id (PK)
├── topic_id (FK -> learning_topics.id)
├── title
├── content_type (text/code/image/video)
├── content
├── order
└── metadata (JSON)

learning_progress
├── id (PK)
├── user_id (FK -> users.id)
├── content_id (FK -> learning_content.id)
├── completed
└── last_accessed
```

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token
- `POST /api/auth/refresh` - Refresh JWT token
- `POST /api/auth/logout` - Logout and invalidate token

### Users

- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update user profile
- `GET /api/users/me/stats` - Get user statistics
- `GET /api/users/me/history` - Get practice history
- `GET /api/users/me/favorites` - Get favorite questions

### Questions

- `GET /api/questions` - List questions with filters
- `GET /api/questions/{id}` - Get question details
- `POST /api/questions/generate` - Generate new question
- `POST /api/questions/{id}/similar` - Generate similar question
- `POST /api/questions/{id}/favorite` - Add to favorites
- `DELETE /api/questions/{id}/favorite` - Remove from favorites

### Submissions

- `POST /api/submissions` - Submit code solution
- `GET /api/submissions` - List user submissions
- `GET /api/submissions/{id}` - Get submission details

### Learning

- `GET /api/learning/categories` - List learning categories
- `GET /api/learning/topics` - List learning topics
- `GET /api/learning/topics/{id}/content` - Get topic content
- `GET /api/learning/content/{id}` - Get specific content
- `POST /api/learning/progress` - Update learning progress

## Frontend Routes

- `/` - Landing page
- `/login` - Login page
- `/register` - Registration page
- `/dashboard` - User dashboard
- `/practice` - Question practice interface
- `/practice/:id` - Specific question practice
- `/companies` - Company-specific questions
- `/companies/:company` - Questions for specific company
- `/learning` - Learning resources
- `/learning/:topic` - Topic-specific learning
- `/profile` - User profile and settings

## Integration with Existing AI Components

The existing AI components from the original InterPrep-AI will be integrated as services in the backend:

1. **Question Generation Service**
   - Moved to `backend/app/ai/gemini.py`
   - Exposed via `/api/questions/generate` endpoint

2. **Solution Evaluation Service**
   - Moved to `backend/app/services/evaluation_service.py`
   - Exposed via `/api/submissions` endpoint

3. **RAG Pipeline**
   - Embeddings generation moved to `backend/app/ai/embeddings.py`
   - FAISS search moved to `backend/app/ai/search.py`
   - Exposed via `/api/questions` endpoint with search parameters

## Learning Resources Structure

Based on "Cracking the Coding Interview" book, the learning resources will be structured as follows:

### Categories

1. **Interview Preparation**
   - The Interview Process
   - Behind the Scenes
   - Special Situations
   - Before the Interview
   - Behavioral Questions

2. **Technical Fundamentals**
   - Big O
   - Technical Questions
   - The Offer and Beyond

3. **Data Structures**
   - Arrays and Strings
   - Linked Lists
   - Stacks and Queues
   - Trees and Graphs

4. **Concepts and Algorithms**
   - Bit Manipulation
   - Math and Logic Puzzles
   - Object-Oriented Design
   - Recursion and Dynamic Programming
   - System Design and Scalability
   - Sorting and Searching
   - Testing

5. **Language-Specific Knowledge**
   - C and C++
   - Java
   - Databases
   - Threads and Locks

6. **Advanced Topics**
   - Useful Math
   - Topological Sort
   - Dijkstra's Algorithm
   - Hash Table Collision Resolution
   - And more...

## Development Workflow

1. **Phase 1: Core Backend Foundation**
   - Set up Flask project structure
   - Implement database models and migrations
   - Create basic API endpoints
   - Integrate existing AI components

2. **Phase 2: Authentication & User Management**
   - Implement user registration and login
   - Set up JWT authentication
   - Create user profiles and settings
   - Add favorites and history tracking

3. **Phase 3: Frontend Foundation & Practice Interface**
   - Set up React project with routing and state management
   - Implement authentication UI
   - Create the split-screen practice interface
   - Connect to backend APIs

4. **Phase 4: Learning Resources Integration**
   - Create database schema for learning content
   - Develop API endpoints for accessing learning materials
   - Build frontend components for displaying learning content
   - Import structured content from "Cracking the Coding Interview"

5. **Phase 5: UI Polish & Personalization**
   - Enhance dashboard with user statistics
   - Implement responsive design
   - Add animations and transitions
   - Optimize performance and user experience
