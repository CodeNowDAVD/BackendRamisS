from pydantic import BaseModel
from typing import Literal

class RQEstadoUpdate(BaseModel):
    estado: Literal["pendiente", "aprobado", "rechazado"]
