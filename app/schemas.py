from pydantic import BaseModel, conlist
from typing import List

class PolygonCreate(BaseModel):
    name: str
    points: List[conlist(float, min_length=2, max_length=2)]

class Polygon(PolygonCreate):
    id: int
