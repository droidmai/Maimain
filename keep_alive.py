from fastapi import FastAPI
from threading import Thread
import uvicorn

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "I'm alive!"}

def run():
    uvicorn.run(app, host="0.0.0.0", port=80)

def keep_alive():
    t = Thread(target=run)
    t.start()