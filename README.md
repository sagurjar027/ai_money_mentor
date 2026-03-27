# AI Money Mentor

AI Money Mentor is a full-stack personal finance app for Indian users. It combines practical calculators, JWT-based authentication, admin controls, MongoDB persistence, and AI-powered guidance in a FastAPI + React application.

## What The App Does

- User signup and login with JWT authentication
- Role-based access with `user` and `admin`
- Health Score calculator with deterministic advice based on the real calculated score
- FIRE Planner for retirement corpus and SIP estimation
- SIP Calculator for monthly investment growth projection
- Tax Calculator for old vs new regime comparison
- General Chat Helper for simple user questions
- Admin dashboard to view users and enable/disable accounts
- MongoDB storage for users and submitted financial records

## Tech Stack

- Backend: FastAPI
- Frontend: React + Vite
- Database: MongoDB
- Auth: JWT + Passlib bcrypt
- Charts: Recharts
- AI: Hugging Face Inference API

## Project Structure

```text
ai-money-mentor/
|-- backend/
|   |-- auth.py
|   |-- db.py
|   |-- main.py
|   |-- models.py
|   `-- routes/
|       |-- auth_routes.py
|       |-- chat.py
|       |-- fire_plan.py
|       |-- health_score.py
|       |-- sip_calc.py
|       `-- tax_calc.py
|-- frontend/
|   |-- package.json
|   |-- vite.config.js
|   |-- .env.example
|   `-- src/
|       |-- components/
|       |-- pages/
|       |   |-- AdminDashboard.jsx
|       |   |-- ChatHelper.jsx
|       |   |-- FirePlanner.jsx
|       |   |-- HealthScore.jsx
|       |   |-- Login.jsx
|       |   |-- SipCalculator.jsx
|       |   |-- Signup.jsx
|       |   `-- TaxCalculator.jsx
|       |-- api.js
|       |-- App.jsx
|       |-- auth.jsx
|       |-- index.css
|       `-- main.jsx
|-- utils/
|   |-- ai_helper.py
|   `-- calculations.py
|-- requirements.txt
`-- README.md
```

## Features

### 1. Health Score

Users enter:
- age
- monthly income
- monthly expenses
- savings
- debt
- investments
- insurance cover

The backend calculates:
- overall score
- category
- score breakdown
- insights
- recommendations

The AI advice for health score is now anchored to the exact calculated output so it does not invent a different score.

### 2. FIRE Planner

Users enter:
- age
- income
- expenses
- savings
- retirement age

The backend returns:
- target corpus
- monthly SIP needed
- years left
- investment strategy
- AI advice

### 3. Tax Calculator

Users enter:
- salary
- 80C investments
- other deductions

The backend returns:
- old regime tax
- new regime tax
- best regime
- suggestions
- AI advice

### 4. SIP Calculator

Users enter:
- monthly SIP amount
- investment duration in years
- expected annual return
- current invested savings

The backend returns:
- projected portfolio value
- total invested amount
- estimated gains
- wealth multiple
- plan outlook
- AI advice

### 5. Chat Helper

Authenticated users can ask a general question and receive an AI-generated response from the `/chat` endpoint.

### 6. Admin Dashboard

Admins can:
- list users
- see status and role
- enable or disable accounts

## Environment Variables

Create a root `.env` file for the backend.

Example:

```env
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=ai_money_mentor
HUGGINGFACE_API_KEY=your_huggingface_api_key
JWT_SECRET_KEY=change_this_to_a_long_random_secret
JWT_EXPIRE_MINUTES=120
```

For the frontend, create `frontend/.env` from `frontend/.env.example`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Installation

### Backend

From the project root:

```bash
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## Run Locally

### Start the backend

From the project root:

```bash
uvicorn backend.main:app --reload
```

You can also run it from inside `backend/`:

```bash
uvicorn main:app --reload
```

Backend default URL:

```text
http://127.0.0.1:8000
```

### Start the frontend

```bash
cd frontend
npm run dev
```

Frontend default URL:

```text
http://127.0.0.1:5173
```

## API Endpoints

### Public

- `POST /signup`
- `POST /login`
- `GET /`

### Authenticated

- `POST /health_score`
- `POST /fire_plan`
- `POST /sip_calc`
- `POST /tax_calc`
- `POST /chat`

### Admin Only

- `GET /admin/users`
- `PATCH /admin/users/{user_id}/status`

## Authentication Flow

- Signup and login both return an `access_token`
- The frontend stores the token in local storage
- Protected API requests send `Authorization: Bearer <token>`
- Disabled users cannot log in or access protected routes

## Notes About AI Advice

- The app uses Hugging Face Inference API from `utils/ai_helper.py`
- Monetary guidance is framed in Indian Rupees by default
- Health score advice uses a dedicated local tool so the explanation stays aligned with the actual score
- SIP calculator advice is generated from the exact projected SIP result returned by the backend
- If the Hugging Face key is missing or the model is unavailable, the app returns a fallback message

## Main Dependencies

Backend dependencies from [requirements.txt](./requirements.txt):

- `fastapi`
- `uvicorn`
- `pydantic`
- `pymongo`
- `python-dotenv`
- `langchain`
- `langchain-huggingface`
- `passlib[bcrypt]`
- `python-jose[cryptography]`

Frontend dependencies:

- `react`
- `react-dom`
- `react-router-dom`
- `axios`
- `recharts`
- `vite`
- `tailwindcss`

## Future Improvements

- Add conversation history for the chat helper
- Add test coverage for routes and utilities
- Add better validation and user-facing error handling
- Add richer admin analytics
- Improve AI advice for FIRE and tax with deterministic helpers similar to health score and SIP
