from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base

class Requerimiento(Base):
    __tablename__ = "requerimientos"

    id = Column(Integer, primary_key=True, index=True)
    solicitante_id = Column(Integer, ForeignKey("users.id"))
    descripcion = Column(String, nullable=True)
    estado = Column(String, default="PENDIENTE")  # PENDIENTE / APROBADO / RECHAZADO
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    solicitante = relationship("User")
    items = relationship("Item", back_populates="requerimiento")
