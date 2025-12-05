# app/schemas/orden_compra_schema.py
from pydantic import BaseModel
from datetime import date
from typing import Optional, List

class OrdenCompraCreate(BaseModel):
    rq_item_id: int
    cantidad_comprada: int
    estado: Optional[str] = "pendiente"
    ubicacion_envio: Optional[str] = None
    fecha: Optional[date] = None
    proveedor: Optional[str] = None
    comprobante: Optional[str] = None
    guia_remision: Optional[str] = None

    # nuevos campos opcionales
    tipo_compra: Optional[str] = None  # "jefe" o "compras"
    costo_envio: Optional[float] = None
    archivo_costo_envio: Optional[str] = None
    notas: Optional[str] = None
class OrdenCompraResponse(BaseModel):
    id: int
    rq_item_id: int
    cantidad_comprada: int
    estado: Optional[str]
    fecha: Optional[date]
    proveedor: Optional[str]
    tipo_compra: Optional[str]

    model_config = {"from_attributes": True}


class OrdenCompraEntity(BaseModel):
    id: int
    rq_item_id: int
    cantidad_comprada: int
    estado: Optional[str] = None
    ubicacion_envio: Optional[str] = None
    fecha: Optional[date] = None
    proveedor: Optional[str] = None
    comprobante: Optional[str] = None
    guia_remision: Optional[str] = None

    tipo_compra: Optional[str] = None
    costo_envio: Optional[float] = None
    archivo_costo_envio: Optional[str] = None
    notas: Optional[str] = None

    model_config = {"from_attributes": True}


class AvanceItem(BaseModel):
    item_id: int
    codigo: str
    descripcion: str
    cantidad_requerida: int
    comprado_antes: int
    comprado_nuevo: int
    comprado_total: int
    avance_efectivo_rq: int
    exceso: int
    progreso: str
    estado_item: str

class EstadoRQResumen(BaseModel):
    rq_id: int
    estado_compra: str
    progreso_compra: float

class OrdenCompraSummaryResponse(BaseModel):
    message: str
    orden: OrdenCompraEntity
    avance_item: AvanceItem
    estado_rq: EstadoRQResumen

    model_config = {"from_attributes": True}
