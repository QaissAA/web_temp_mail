Temporary Email Service

Overview

Temporary Email Service is a web-based application that allows users to generate temporary email addresses, receive emails, and automatically delete expired emails after a set duration (10 minutes). The application consists of a FastAPI backend and a simple HTML, CSS, and JavaScript frontend.

Features

Generate a temporary email address

Receive emails sent to the temporary address

Emails expire and are deleted after 10 minutes

Automatic cleanup of expired emails

Simple frontend interface for interaction

Technology Stack

Backend:

FastAPI (Python)

MongoDB (Database)

Pydantic (Data validation)

UUID (Unique email generation)

asyncio (Background cleanup tasks)

CORS Middleware (Cross-Origin Requests support)

Frontend:

HTML

CSS

JavaScript (Fetch API for interacting with backend)

Installation

Prerequisites:

Python 3.8+

MongoDB installed and running

Node.js (Optional for frontend development)

Clone the Repository:

git clone https://github.com/QaissAA/web_temp_mail
cd temp-email-service

Backend Setup:

Install dependencies:

pip install fastapi uvicorn pymongo pydantic

Start MongoDB:

mongod --dbpath /path/to/your/db

Run the FastAPI server:

uvicorn main:app --reload

The API will be available at: http://localhost:8000

Frontend Setup:

Simply open index.html in a browser. The frontend will interact with the backend via JavaScript.

API Endpoints

1. Generate Temporary Email

Endpoint: POST /generate-email/

Response:

{
  "temp_email": "a1b2c3d4@tempmail.local",
  "expires_at": "2025-02-25T12:00:00"
}

2. Get Emails for a Temporary Address

Endpoint: GET /emails/{temp_email}

Response:

[
  {
    "sender": "test@example.com",
    "subject": "Welcome!",
    "body": "Hello, this is a test email.",
    "received_at": "2025-02-25T11:50:00"
  }
]

3. Receive a New Email (Simulated)

Endpoint: POST /receive-email/{temp_email}

Request Body:

{
  "sender": "test@example.com",
  "subject": "Test Email",
  "body": "This is a test email.",
  "received_at": "2025-02-25T11:55:00"
}

Response:

{"message": "Email received successfully"}

Background Cleanup Task

The backend automatically deletes expired emails every 60 seconds using an asyncio task.

Running in Production

Use a production-grade ASGI server like gunicorn with uvicorn:

gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app



Authors: Kaisarov Alikhan, Ilyas Kairzhanuly



