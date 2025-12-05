from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from app.schemas.rq_item_schema import RQItemResponse

class RQCreate(BaseModel):
    nro_rq: str
    proyecto: str
    solicitante: str
    fecha_emision: date
    estado: Optional[str] = "pendiente"
    items: List[dict]  # lista de RQItemCreate como diccionarios

class RQResponse(BaseModel):
    id: int
    nro_rq: str
    proyecto: str
    solicitante: str
    fecha_emision: date
    estado: str
    estado_compra: str
    progreso_compra: float
    items: List[RQItemResponse] = []

    model_config = {"from_attributes": True}
