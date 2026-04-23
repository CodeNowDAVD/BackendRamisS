from __future__ import annotations

from typing import List

from pydantic import BaseModel, ConfigDict


class RQItemCompraEstado(BaseModel):
    item_id: int
    codigo: str
    descripcion: str
    cantidad_pedida: int
    cantidad_comprada: int
    cantidad_faltante: int
    progreso: float  # %

    model_config = ConfigDict(from_attributes=True)


class RQCompraEstadoResponse(BaseModel):
    rq_id: int
    nro_rq: str
    estado_compra: str
    progreso_compra: float
    items: List[RQItemCompraEstado]

    model_config = ConfigDict(from_attributes=True)
