# app/schemas/almacen.py

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class TipoArticuloSchema(str, Enum):
    EQUIPO = "equipo"
    CONSUMIBLE = "consumible"
class ArticuloSchema(BaseModel):
    id: int
    nombre: str
    unidad_medida: str
    tipo: TipoArticuloSchema
    stock_actual: int
    codigo_excel: str

    model_config = ConfigDict(from_attributes=True)