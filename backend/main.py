from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TaskCreate(BaseModel):
    title: str
    done: bool = False


class Task(BaseModel):
    id: int
    title: str
    done: bool


tasks: dict[int, Task] = {}
next_id: int = 1


@app.get("/tasks")
def list_tasks() -> list[Task]:
    return list(tasks.values())


@app.get("/tasks/{task_id}")
def get_task(task_id: int) -> Task:
    if task_id not in tasks:
        raise HTTPException(404, "Task not found")
    return tasks[task_id]


@app.post("/tasks", status_code=201)
def create_task(body: TaskCreate) -> Task:
    global next_id
    task = Task(id=next_id, **body.model_dump())
    tasks[next_id] = task
    next_id += 1
    return task


@app.patch("/tasks/{task_id}")
def update_task(task_id: int, body: TaskCreate) -> Task:
    if task_id not in tasks:
        raise HTTPException(404, "Task not found")
    tasks[task_id] = Task(id=task_id, **body.model_dump())
    return tasks[task_id]


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int) -> None:
    if task_id not in tasks:
        raise HTTPException(404, "Task not found")
    del tasks[task_id]
