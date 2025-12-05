# app/repositories/rq_repository.py
from sqlalchemy.orm import Session
from app.models.rq_model import Requerimiento

class RQRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, rq: Requerimiento):
        self.db.add(rq)
        self.db.commit()
        self.db.refresh(rq)
        return rq

    def get_all(self):
        return self.db.query(Requerimiento).all()

    def get_by_id(self, rq_id: int):
        return self.db.query(Requerimiento).filter(Requerimiento.id == rq_id).first()

    def update_estado(self, rq_id: int, estado: str):
        rq = self.get_by_id(rq_id)
        if not rq:
            return None
        rq.estado = estado
        self.db.commit()
        self.db.refresh(rq)
        return rq

    def delete(self, rq_id: int):
        rq = self.get_by_id(rq_id)
        if not rq:
            return None
        self.db.delete(rq)
        self.db.commit()
        return rq
