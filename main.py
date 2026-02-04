from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import redis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[allow_origins=["https://nm202644.github.io", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_redis():
    return redis.from_url(os.environ["REDIS_URL"])

def load_votes(r):
    data = r.get("votes")
    if data:
        return json.loads(data)
    return {"crisis":0,"highly-stressed":0,"concerned":0,"neutral":0,"very-good":0,"thriving":0}

def save_votes(r, data):
    r.set("votes", json.dumps(data))

@app.get("/")
async def root():
    return {"message": "Temp Check API running"}

@app.get("/results")
async def results():
    r = get_redis()
    return load_votes(r)

@app.post("/vote")
async def vote(request: Request):
    body = await request.body()
    vote_data = json.loads(body)
    r = get_redis()
    data = load_votes(r)
    value = vote_data.get("value")
    if value in data:
        data[value] += 1
    save_votes(r, data)
    return data

@app.post("/reset")
async def reset_votes():
    r = get_redis()
    data = {"crisis":0,"highly-stressed":0,"concerned":0,"neutral":0,"very-good":0,"thriving":0}
    save_votes(r, data)
    return {"message": "Reset successful"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
