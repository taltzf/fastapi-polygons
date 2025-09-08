from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import polygon
from app.database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(polygon.router, prefix="/api")

# Serve static files
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")
