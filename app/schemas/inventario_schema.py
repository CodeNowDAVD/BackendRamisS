from pydantic import BaseModel
from typing import Optional

class InventarioCreate(BaseModel):
    codigo: str
    descripcion: str
    cantidad_disponible: int
    ubicacion: str
    rq_item_id: Optional[int] = None  # si proviene de un RQItem

class InventarioResponse(BaseModel):
    id: int
    codigo: str
    descripcion: str
    cantidad_disponible: int
    ubicacion: str
    rq_item_id: Optional[int] = None

    model_config = {"from_attributes": True}
