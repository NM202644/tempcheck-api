from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

data = {"crisis":0,"highly-stressed":0,"concerned":0,"neutral":0,"very-good":0,"thriving":0}

@app.get("/results")
async def results():
    return data

@app.post("/vote")
async def vote(vote: dict):
    value = vote.get("value")
    if value in data:
        data[value] += 1
    return data
