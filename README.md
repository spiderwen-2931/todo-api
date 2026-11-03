# TODO API

A simple REST API built with FastAPI for the DevOps Assignment (Component 1).

## Endpoints
- GET  /health       - Health check
- POST /todos/       - Create a todo
- GET  /todos/       - List all todos
- GET  /todos/{id}   - Get a todo by ID
- PUT  /todos/{id}   - Update a todo
- DELETE /todos/{id} - Delete a todo

## Run locally
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080

## Run tests
pytest tests/ -v
