from fastapi import FastAPI
from app.routers import polygon
from app.database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(polygon.router, prefix="/api")
