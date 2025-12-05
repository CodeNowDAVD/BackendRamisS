from sqlalchemy.orm import Session
from app.models.orden_compra_model import OrdenCompraParcial

class OrdenCompraRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, orden: OrdenCompraParcial):
        self.db.add(orden)
        self.db.commit()
        self.db.refresh(orden)
        return orden

    def get_by_item(self, rq_item_id: int):
        return self.db.query(OrdenCompraParcial).filter(OrdenCompraParcial.rq_item_id == rq_item_id).all()

    def get_by_id(self, orden_id: int):
        return self.db.query(OrdenCompraParcial).filter(OrdenCompraParcial.id == orden_id).first()

    def update(self, orden_id: int, **kwargs):
        orden = self.get_by_id(orden_id)
        if not orden:
            return None
        for key, value in kwargs.items():
            setattr(orden, key, value)
        self.db.commit()
        self.db.refresh(orden)
        return orden

    def delete(self, orden_id: int):
        orden = self.get_by_id(orden_id)
        if not orden:
            return None
        self.db.delete(orden)
        self.db.commit()
        return orden
