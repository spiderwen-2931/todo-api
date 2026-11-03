from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas import TodoCreate, TodoUpdate, TodoResponse
import app.crud as crud

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate):
    """Create a new TODO item."""
    return crud.create_todo(payload)


@router.get("/", response_model=List[TodoResponse])
def list_todos():
    """Retrieve all TODO items."""
    return crud.get_all_todos()


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int):
    """Retrieve a single TODO item by ID."""
    todo = crud.get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail=f"TODO with id={todo_id} not found")
    return todo


@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, payload: TodoUpdate):
    """Update an existing TODO item (partial update supported)."""
    todo = crud.update_todo(todo_id, payload)
    if not todo:
        raise HTTPException(status_code=404, detail=f"TODO with id={todo_id} not found")
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int):
    """Delete a TODO item by ID."""
    deleted = crud.delete_todo(todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"TODO with id={todo_id} not found")
