# Standard library imports
import os

# Third-party imports
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from databases import Database

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")
database = Database(DATABASE_URL)

templates = Jinja2Templates(directory="static/templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/health", response_class=HTMLResponse)
async def health_check(request: Request):
    status = "we good"
    return templates.TemplateResponse("health.html", {"request": request, "status": status})

@app.get("/battlebros/builds", response_class=HTMLResponse)
async def get_builds(request: Request):
    query = "SELECT * FROM BattleBros WHERE type = 'build';"
    rows = await database.fetch_all(query=query)
    
    results = []
    for row in rows:
        row_dict = dict(row)
        filtered = {k: v for k, v in row_dict.items() if v is not None and v != "0" and v != "build" and k != "id"}
        results.append(filtered)

    return templates.TemplateResponse("builds.html", {"request": request, "builds": results})

