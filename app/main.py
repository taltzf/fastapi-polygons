from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import polygon

app = FastAPI()
app.include_router(polygon.router, prefix="/api")

# Serve static files
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
