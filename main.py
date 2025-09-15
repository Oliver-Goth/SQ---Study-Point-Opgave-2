import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Task Manager API")

# Task model

class Task(BaseModel):
    id: int = None  
    title: str
    description: str
    done: bool = False

# File to store tasks

TASK_FILE = "tasks.json"

# Load tasks from file

def load_tasks() -> List[Task]:
    try:
        with open(TASK_FILE, "r") as f:
            tasks_data = json.load(f)
            return [Task(**task) for task in tasks_data]
    except FileNotFoundError:
        return []


# Save tasks to file

def save_tasks(tasks: List[Task]):
    with open(TASK_FILE, "w") as f:
        json.dump([task.dict() for task in tasks], f, indent=4)


# In-memory storage

tasks: List[Task] = load_tasks()


# Generate new unique ID

def get_next_id() -> int:
    if tasks:
        return max(task.id for task in tasks) + 1
    return 1


# Root endpoint

@app.get("/")
def root():
    return {"message": "Task Manager API with auto IDs is running"}


# CREATE

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    task.id = get_next_id()
    tasks.append(task)
    save_tasks(tasks)
    return task


# READ ALL

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

# READ ONE
@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for t in tasks:
        if t.id == task_id:
            return t
    raise HTTPException(status_code=404, detail="Task not found")


# UPDATE
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, updated_task: Task):
    for index, t in enumerate(tasks):
        if t.id == task_id:
            updated_task.id = task_id
            tasks[index] = updated_task
            save_tasks(tasks)
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")


# DELETE

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, t in enumerate(tasks):
        if t.id == task_id:
            tasks.pop(index)
            save_tasks(tasks)
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")
