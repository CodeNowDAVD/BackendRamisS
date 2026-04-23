from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, ConfigDict


class TipoArticuloSchema(str, Enum):
    EQUIPO = "equipo"
    CONSUMIBLE = "consumible"


class ItemPrestamo(BaseModel):
    articulo_id: int
    cantidad: int


class PrestamoDetalleSchema(BaseModel):
    id: int
    articulo_id: int
    cantidad_prestada: int
    cantidad_devuelta: int
    esta_devuelto: bool
    articulo_nombre: str
    articulo_tipo: str
    articulo_unidad: str

    model_config = ConfigDict(from_attributes=True)


class PrestamoQRData(BaseModel):
    trabajador_id: int
    codigo_unico: str
    dni: str
    nombres_completos: str
    cargo: str
    fecha_prestamo: datetime
    fecha_devolucion_prevista: datetime
    items: List[ItemPrestamo]
    firma_base64: str


class PrestamoResponse(BaseModel):
    id: int
    codigo_unico: str
    estado: str
    message: str = "Préstamo registrado correctamente"


class ArticuloPrestamoSchema(BaseModel):
    trabajador_id: int
    nombres_completos: str
    dni: str
    cargo: str
    fecha_prestamo: datetime
    cantidad_pendiente: int


class PrestamoSchema(BaseModel):
    id: int
    trabajador_id: int
    nombres_completos: str
    dni: str
    cargo: str
    codigo_unico: str
    fecha_prestamo: datetime
    fecha_devolucion_prevista: datetime
    firma_base64: str
    estado: str
    registrado_por: str
    fecha_registro: datetime
    detalles: List[PrestamoDetalleSchema]

    model_config = ConfigDict(from_attributes=True)
