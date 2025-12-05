from sqlalchemy.orm import Session
from app.models.inventario_model import Inventario

class InventarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, item: Inventario):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_by_codigo(self, codigo: str):
        return self.db.query(Inventario).filter(Inventario.codigo == codigo).first()

    def get_all(self):
        return self.db.query(Inventario).all()

    def update_cantidad(self, inventario_id: int, cantidad: int):
        item = self.db.query(Inventario).filter(Inventario.id == inventario_id).first()
        if not item:
            return None
        item.cantidad_disponible = cantidad
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, inventario_id: int):
        item = self.db.query(Inventario).filter(Inventario.id == inventario_id).first()
        if not item:
            return None
        self.db.delete(item)
        self.db.commit()
        return item
