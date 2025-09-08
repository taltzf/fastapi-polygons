import json
from sqlalchemy.orm import Session
from app import models, schemas

def create_polygon(db: Session, polygon: schemas.PolygonCreate):
    db_polygon = models.PolygonModel(
        name=polygon.name,
        points=json.dumps(polygon.points)
    )
    db.add(db_polygon)
    db.commit()
    db.refresh(db_polygon)
    return db_polygon

def get_polygons(db: Session):
    return db.query(models.PolygonModel).all()

def delete_polygon(db: Session, polygon_id: int) -> bool:
    polygon = db.query(models.PolygonModel).filter(models.PolygonModel.id == polygon_id).first()
    if polygon:
        db.delete(polygon)
        db.commit()
        return True
    return False
