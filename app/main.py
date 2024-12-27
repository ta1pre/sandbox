# app/main.py

from fastapi import FastAPI
from app.db.check import test_db_connection

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI app!"}

@app.get("/db-check/")
async def db_check():
    if test_db_connection():
        return {"message": "✅ Database connection successful!"}
    else:
        return {"message": "❌ Database connection failed. Check logs for more details."}
