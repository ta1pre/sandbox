# app/main.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "1229！"}

@app.get("/test")
async def root():
    return {"message": "てすとぺーじ"}

