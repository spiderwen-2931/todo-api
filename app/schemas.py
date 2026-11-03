from pydantic import BaseModel, Field
from typing import Optional


class TodoCreate(BaseModel):
    """Schema for creating a new TODO item."""
    title: str = Field(..., min_length=1, max_length=255, description="Title of the TODO item")
    description: Optional[str] = Field(None, max_length=1000, description="Optional description")
    completed: bool = Field(False, description="Whether the task is completed")


class TodoUpdate(BaseModel):
    """Schema for updating an existing TODO item (all fields optional)."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None


class TodoResponse(BaseModel):
    """Schema for a TODO item in API responses."""
    id: int
    title: str
    description: Optional[str]
    completed: bool

    class Config:
        from_attributes = True
