import pytest
from main import Task, tasks, save_tasks
import requests

BASE_URL = "http://127.0.0.1:8000"


# Unit Tests (in-memory)

def test_create_task_unit():
    tasks.clear()
    task = Task(id=1, title="Unit Test Task", description="Test", done=False)
    tasks.append(task)
    assert len(tasks) == 1
    assert tasks[0].title == "Unit Test Task"

def test_update_task_unit():
    tasks.clear()
    task = Task(id=1, title="Old Task", description="Update Test", done=False)
    tasks.append(task)
    updated_task = Task(id=1, title="Updated Task", description="Updated", done=True)
    tasks[0] = updated_task
    assert tasks[0].title == "Updated Task"
    assert tasks[0].done is True

def test_delete_task_unit():
    tasks.clear()
    task = Task(id=1, title="Delete Task", description="Delete Test", done=False)
    tasks.append(task)
    tasks.pop(0)
    assert len(tasks) == 0


# Integration Tests (API)

def test_api_create_task():
    response = requests.post(f"{BASE_URL}/tasks", json={
        "title": "API Task",
        "description": "Integration Test"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "API Task"
    assert data["done"] is False

def test_api_get_tasks():
    response = requests.get(f"{BASE_URL}/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_api_update_task():
    response = requests.put(f"{BASE_URL}/tasks/1", json={
        "title": "Updated API Task",
        "description": "Updated",
        "done": True
    })
    assert response.status_code == 200
    data = response.json()
    assert data["done"] is True

def test_api_delete_task():
    response = requests.delete(f"{BASE_URL}/tasks/1")
    assert response.status_code == 200
    data = response.json()
    assert "deleted" in data["message"].lower()
