from fastapi import FastAPI
from app.router import router

app = FastAPI(
    title="TODO API",
    description="A simple TODO REST API built with FastAPI — DevOps Assignment Component 1",
    version="1.0.0",
)

app.include_router(router)


@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint — used by CI/CD pipelines."""
    return {"status": "ok", "service": "todo-api"}
