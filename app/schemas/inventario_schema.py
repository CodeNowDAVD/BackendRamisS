from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class InventarioEntity(BaseModel):
    """Esquema de respuesta para un solo ítem de inventario."""
    id: int
    codigo: str
    descripcion: str
    cantidad_disponible: int
    ubicacion: Optional[str] = None
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    model_config = ConfigDict(from_attributes=True)


class InventarioListResponse(BaseModel):
    """Esquema para listar el inventario completo."""
    items: List[InventarioEntity]
    total_items: int

    model_config = ConfigDict(from_attributes=True)