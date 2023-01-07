# main.py

import os

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/waterpolo/{competition_id}/{teamname}")
async def read_item(competition_id: str, teamname: str):
    return {"competition": competition_id, "team": teamname}


@app.get("/index.html")
async def read_html():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    with open(file_path, encoding='utf-8') as f:
        return f.read()

