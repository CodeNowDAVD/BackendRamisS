from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.base import Base

class Inventario(Base):
    __tablename__ = "inventario"
    id = Column(Integer, primary_key=True)
    codigo = Column(String)
    descripcion = Column(String)
    cantidad_disponible = Column(Integer)
    unidad = Column(String)
    ubicacion = Column(String)
    rq_item_id = Column(Integer, ForeignKey("rq_items.id"), nullable=True)
