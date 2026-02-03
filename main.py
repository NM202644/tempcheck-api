from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://nm202644.github.io/tempcheck/", "*"],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

def load_votes():
    try:
        stored = os.environ.get("VOTES_DATA")
        if stored:
            return json.loads(stored)
    except:
        pass
    return {"crisis":0,"highly-stressed":0,"concerned":0,"neutral":0,"very-good":0,"thriving":0}

def save_votes(data):
    os.environ["VOTES_DATA"] = json.dumps(data)

@app.get("/")
async def root():
    return {"message": "Temp Check API running"}

@app.get("/results")
async def results():
    return load_votes()

@app.post("/vote")
async def vote(request: Request):
    body = await request.body()
    vote_data = json.loads(body)
    data = load_votes()
    value = vote_data.get("value")
    if value in data:
        data[value] += 1
    save_votes(data)
    return data

@app.post("/reset")
async def reset_votes():
    data = {"crisis":0,"highly-stressed":0,"concerned":0,"neutral":0,"very-good":0,"thriving":0}
    save_votes(data)
    return {"message": "Reset successful"}
