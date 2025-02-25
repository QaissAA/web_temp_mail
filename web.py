from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from uuid import uuid4
from datetime import datetime, timedelta
import asyncio
from pymongo import MongoClient

app = FastAPI()

client = MongoClient("mongodb://localhost:27017")
db = client.temp_mail
temp_emails_collection = db.temp_emails

temp_emails_collection.create_index("temp_email", unique=True)
temp_emails_collection.create_index("expires_at", expireAfterSeconds=600)  # Автоматическое удаление через 10 мин

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модель письма
class Email(BaseModel):
    sender: str
    subject: str
    body: str
    received_at: datetime

# Генерация временного email
@app.post("/generate-email/")
def generate_email():
    unique_id = uuid4().hex[:8]
    temp_email = f"{unique_id}@tempmail.local"
    expiration = datetime.utcnow() + timedelta(minutes=10)
    
    temp_emails_collection.insert_one({
        "temp_email": temp_email,
        "emails": [],
        "expires_at": expiration
    })

    return {"temp_email": temp_email, "expires_at": expiration}

# Получение писем
@app.get("/emails/{temp_email}", response_model=List[Email])
def get_emails(temp_email: str):
    temp_email_data = temp_emails_collection.find_one({"temp_email": temp_email})
    
    if not temp_email_data:
        raise HTTPException(status_code=404, detail="Temporary email not found")
    
    if temp_email_data["expires_at"] < datetime.utcnow():
        temp_emails_collection.delete_one({"temp_email": temp_email})
        raise HTTPException(status_code=404, detail="Temporary email has expired")
    
    return [Email(**email) for email in temp_email_data["emails"]]

# Получение нового письма
@app.post("/receive-email/{temp_email}")
def receive_email(temp_email: str, email: Email):
    temp_email_data = temp_emails_collection.find_one({"temp_email": temp_email})
    
    if not temp_email_data:
        raise HTTPException(status_code=404, detail="Temporary email not found")
    
    if temp_email_data["expires_at"] < datetime.utcnow():
        temp_emails_collection.delete_one({"temp_email": temp_email})
        raise HTTPException(status_code=404, detail="Temporary email has expired")

    temp_emails_collection.update_one(
        {"temp_email": temp_email},
        {"$push": {"emails": email.dict()}}
    )

    return {"message": "Email received successfully"}

# Фоновая очистка писем
async def cleanup_emails():
    while True:
        temp_emails_collection.delete_many({"expires_at": {"$lt": datetime.utcnow()}})
        await asyncio.sleep(60)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(cleanup_emails())
