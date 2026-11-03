from typing import Dict, List, Optional
from app.schemas import TodoCreate, TodoUpdate, TodoResponse


# In-memory data store (simulates a database)
_todos: Dict[int, dict] = {}
_next_id: int = 1


def _reset():
    """Reset the store — used in tests."""
    global _todos, _next_id
    _todos = {}
    _next_id = 1


def create_todo(data: TodoCreate) -> TodoResponse:
    global _next_id
    todo = {
        "id": _next_id,
        "title": data.title,
        "description": data.description,
        "completed": data.completed,
    }
    _todos[_next_id] = todo
    _next_id += 1
    return TodoResponse(**todo)


def get_all_todos() -> List[TodoResponse]:
    return [TodoResponse(**t) for t in _todos.values()]


def get_todo(todo_id: int) -> Optional[TodoResponse]:
    todo = _todos.get(todo_id)
    return TodoResponse(**todo) if todo else None


def update_todo(todo_id: int, data: TodoUpdate) -> Optional[TodoResponse]:
    todo = _todos.get(todo_id)
    if not todo:
        return None
    if data.title is not None:
        todo["title"] = data.title
    if data.description is not None:
        todo["description"] = data.description
    if data.completed is not None:
        todo["completed"] = data.completed
    _todos[todo_id] = todo
    return TodoResponse(**todo)


def delete_todo(todo_id: int) -> bool:
    if todo_id not in _todos:
        return False
    del _todos[todo_id]
    return True
