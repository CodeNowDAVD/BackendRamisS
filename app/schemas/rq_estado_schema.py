from pydantic import BaseModel
from typing import Literal
from __future__ import annotations

class RQEstadoUpdate(BaseModel):
    estado: Literal["pendiente", "aprobado", "rechazado"]
