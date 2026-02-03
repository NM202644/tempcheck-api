from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

data = {"crisis":0,"highly-stressed":0,"concerned":0,"neutral":0,"very-good":0,"thriving":0}

@app.get("/")
async def root():
    return {"message": "Temp Check API running"}

@app.get("/results")
async def results():
    return data

@app.post("/vote")
async def vote(request: Request):
    body = await request.body()
    vote_data = json.loads(body)
    value = vote_data.get("value")
    if value in data:
        data[value] += 1
    return data
