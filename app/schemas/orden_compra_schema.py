# app/schemas/orden_compra_schema.py
from __future__ import annotations

from datetime import date
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

MERCADERIA_COMPROBANTE = "MERCADERIA_COMPROBANTE"
ENVIO_COMPROBANTE = "ENVIO_COMPROBANTE"
GUIA_REMISION = "GUIA_REMISION"
XML_MERCADERIA = "XML_MERCADERIA"
XML_ENVIO = "XML_ENVIO"


class ComprobanteItem(BaseModel):
    tipo_documento: str = Field(..., description="Tipo de documento subido (e.g., MERCADERIA_COMPROBANTE)")
    archivo_ruta: str = Field(..., description="Ruta o URL del archivo subido")
    numero_comprobante: Optional[str] = None
    es_factura: Optional[bool] = None
    fecha: Optional[date] = None

    @model_validator(mode="after")
    def validate_es_factura_and_number(self) -> ComprobanteItem:
        doc_type = self.tipo_documento
        number = self.numero_comprobante
        v = self.es_factura

        is_comprobante = doc_type in [MERCADERIA_COMPROBANTE, ENVIO_COMPROBANTE]
        is_auxiliary = doc_type in [GUIA_REMISION, XML_MERCADERIA, XML_ENVIO]

        if is_comprobante:
            if v is None:
                raise ValueError(f"Para {doc_type}, 'es_factura' (True/False) es obligatorio.")
            if not number:
                raise ValueError(f"Para {doc_type}, el 'numero_comprobante' es obligatorio.")

        if is_auxiliary and v is not None:
            raise ValueError(f"Para {doc_type}, 'es_factura' debe ser nulo.")

        return self


class DocumentoCreateItem(BaseModel):
    tipo: str
    archivo: str
    fecha: Optional[date] = None


class OrdenCompraItemCreate(BaseModel):
    rq_item_id: int = Field(..., description="ID del RQItem al que se asigna la compra.")
    cantidad_comprada: int
    costo_unitario: Optional[float] = None


class OrdenCompraCreate(BaseModel):
    estado: Optional[str] = "comprado"
    ubicacion_envio: Optional[str] = None
    fecha: Optional[date] = None
    proveedor: Optional[str] = None
    tipo_compra: Literal["ENVIO", "FISICA"] = Field(..., description="Tipo de compra: ENVIO o FISICA")
    costo_envio: Optional[float] = None
    notas: Optional[str] = None
    items_comprados: List[OrdenCompraItemCreate]
    comprobantes: List[ComprobanteItem]

    @field_validator("items_comprados")
    @classmethod
    def validar_items_comprados(cls, v: List[OrdenCompraItemCreate]) -> List[OrdenCompraItemCreate]:
        if not v or len(v) == 0:
            raise ValueError("La orden de compra debe tener al menos un ítem comprado.")
        return v

    @model_validator(mode="after")
    def validar_comprobantes_minimos(self) -> OrdenCompraCreate:
        comprobantes = self.comprobantes
        tipo_compra = self.tipo_compra

        if not comprobantes or len(comprobantes) == 0:
            raise ValueError("Debe adjuntar al menos un comprobante.")

        tipos = [c.tipo_documento for c in comprobantes]

        if len(tipos) != len(set(tipos)):
            raise ValueError("No se permiten comprobantes duplicados del mismo tipo.")

        archivos = set(tipos)

        if MERCADERIA_COMPROBANTE not in archivos:
            raise ValueError("Es obligatorio adjuntar comprobante de mercadería.")

        if tipo_compra == "FISICA":
            prohibidos = {ENVIO_COMPROBANTE, XML_ENVIO}
            if archivos & prohibidos:
                raise ValueError("Compra FÍSICA no puede incluir comprobantes de envío.")

        if tipo_compra == "ENVIO":
            obligatorios = {
                MERCADERIA_COMPROBANTE,
                ENVIO_COMPROBANTE,
                GUIA_REMISION,
            }
            faltantes = obligatorios - archivos
            if faltantes:
                raise ValueError(
                    f"Para compra por ENVÍO faltan comprobantes obligatorios: {', '.join(faltantes)}"
                )

        return self


class ComprobanteEntity(BaseModel):
    id: int
    tipo_documento: str
    archivo_ruta: str
    numero_comprobante: Optional[str] = None
    es_factura: Optional[bool] = None
    fecha: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)


class OrdenCompraEntity(BaseModel):
    id: int
    estado: Optional[str] = None
    ubicacion_envio: Optional[str] = None
    fecha: Optional[date] = None
    proveedor: Optional[str] = None
    tipo_compra: Optional[str] = None
    costo_envio: Optional[float] = None
    notas: Optional[str] = None
    items_comprados: List[Dict[str, Any]] = Field(default_factory=list)
    comprobantes: List[ComprobanteEntity] = Field(default_factory=list)


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


class OrdenCompraResponse(BaseModel):
    id: int
    estado: Optional[str]
    fecha: Optional[date]
    proveedor: Optional[str]
    tipo_compra: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class EstadoRQResumen(BaseModel):
    rq_id: int
    estado_compra: str
    progreso_compra: float


class OrdenCompraSummaryResponse(BaseModel):
    message: str
    orden: OrdenCompraEntity
    avance_item: AvanceItem
    estado_rq: EstadoRQResumen

    model_config = ConfigDict(from_attributes=True)


class ComprobanteCreateItem(BaseModel):
    tipo_documento: str = Field(..., description="Tipo de documento subido (e.g., MERCADERIA_COMPROBANTE)")
    archivo_ruta: str = Field(..., description="Ruta o URL del archivo subido")
    numero_comprobante: Optional[str] = None
    es_factura: Optional[bool] = None
    fecha: Optional[date] = None


class OrdenCompraItemUpdateCantidad(BaseModel):
    nueva_cantidad: int


class OrdenCompraPatch(BaseModel):
    """Esquema para la actualización parcial (PATCH) de la cabecera de la Orden."""

    estado: Optional[str] = None
    ubicacion_envio: Optional[str] = None
    fecha: Optional[date] = None
    proveedor: Optional[str] = None
    tipo_compra: Optional[Literal["ENVIO", "FISICA"]] = None
    costo_envio: Optional[float] = None
    notas: Optional[str] = None
    comprobantes_adicionales: Optional[List[ComprobanteCreateItem]] = Field(
        None,
        description="Lista de comprobantes adicionales a agregar, sin reemplazar los existentes.",
    )

    model_config = ConfigDict(extra="ignore")
