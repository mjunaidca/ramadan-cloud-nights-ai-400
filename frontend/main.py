import os

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

API_URL = os.getenv("API_URL", "http://localhost:8000")


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/tasks")
async def get_tasks():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_URL}/tasks")
    return JSONResponse(resp.json(), status_code=resp.status_code)


@app.get("/api/tasks/{task_id}")
async def get_task(task_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_URL}/tasks/{task_id}")
    return JSONResponse(resp.json(), status_code=resp.status_code)


@app.post("/api/tasks")
async def create_task(request: Request):
    body = await request.json()
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_URL}/tasks", json=body)
    return JSONResponse(resp.json(), status_code=resp.status_code)


@app.patch("/api/tasks/{task_id}")
async def update_task(task_id: int, request: Request):
    body = await request.json()
    async with httpx.AsyncClient() as client:
        resp = await client.patch(f"{API_URL}/tasks/{task_id}", json=body)
    return JSONResponse(resp.json(), status_code=resp.status_code)


@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.delete(f"{API_URL}/tasks/{task_id}")
    return JSONResponse(resp.json(), status_code=resp.status_code)
