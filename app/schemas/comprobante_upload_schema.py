from pydantic import BaseModel
from datetime import date
from typing import Optional
from __future__ import annotations

class ComprobanteUploadData(BaseModel):
    tipo_documento: str
    numero_comprobante: Optional[str] = None
    es_factura: Optional[bool] = None
    fecha: Optional[date] = None
