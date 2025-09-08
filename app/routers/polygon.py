from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, database
import json

router = APIRouter()

@router.post("/polygon/", response_model=schemas.Polygon)
def create_polygon(polygon: schemas.PolygonCreate, db: Session = Depends(database.get_db)):
    db_polygon = crud.create_polygon(db, polygon)
    return schemas.Polygon(id=db_polygon.id, name=db_polygon.name, points=polygon.points)

@router.get("/polygons/", response_model=list[schemas.Polygon])
def fetch_polygons(db: Session = Depends(database.get_db)):
    db_polygons = crud.get_polygons(db)
    return [schemas.Polygon(id=p.id, name=p.name, points=json.loads(p.points)) for p in db_polygons]

@router.delete("/polygon/{polygon_id}", response_model=dict)
def delete_polygon(polygon_id: int, db: Session = Depends(database.get_db)):
    success = crud.delete_polygon(db, polygon_id)
    if not success:
        raise HTTPException(status_code=404, detail="Polygon not found")
    return {"message": f"Polygon {polygon_id} deleted"}
