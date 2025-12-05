from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base

class OrdenCompraParcial(Base):
    __tablename__ = "ordenes_parciales"
    id = Column(Integer, primary_key=True)
    rq_item_id = Column(Integer, ForeignKey("rq_items.id"))
    cantidad_comprada = Column(Integer)
    cantidad_restante = Column(Integer, nullable=True)
    estado = Column(String, default="pendiente")  # pendiente, comprando, por_completar, comprado
    ubicacion_envio = Column(String, nullable=True)
    proveedor = Column(String, nullable=True)
    fecha = Column(Date, nullable=True)
    comprobante = Column(String, nullable=True)  # archivo subido
    guia_remision = Column(String, nullable=True)  # archivo subido si aplica

    # NUEVOS CAMPOS
    tipo_compra = Column(String, nullable=True)  # jefe | compras
    costo_envio = Column(Float, nullable=True)
    archivo_costo_envio = Column(String, nullable=True)
    notas = Column(String, nullable=True)

    rq_item = relationship("RQItem", back_populates="ordenes_parciales")
