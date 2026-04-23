from __future__ import annotations

from datetime import date
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.rq_item_schema import RQItemResponse


class RQCreate(BaseModel):
    nro_rq: str
    proyecto: str
    solicitante: str
    fecha_emision: date
    estado: Optional[str] = "pendiente"
    items: List[dict]


class RQResponse(BaseModel):
    id: int
    nro_rq: str
    proyecto: str
    solicitante: str
    fecha_emision: date
    estado: str
    estado_compra: str
    progreso_compra: float
    items: List[RQItemResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
