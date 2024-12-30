# app/main.py

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "1230！"}

@app.get("/test")
async def test():
    return {"message": "てすとぺーじ"}

