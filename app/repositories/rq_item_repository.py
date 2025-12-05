from sqlalchemy.orm import Session
from app.models.rq_item_model import RQItem

class RQItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, item: RQItem):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_by_rq(self, rq_id: int):
        return self.db.query(RQItem).filter(RQItem.rq_id == rq_id).all()

    def get_by_id(self, item_id: int):
        return self.db.query(RQItem).filter(RQItem.id == item_id).first()

    def update_estado(self, item_id: int, estado: str):
        item = self.get_by_id(item_id)
        if not item:
            return None
        item.estado = estado
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item_id: int):
        item = self.get_by_id(item_id)
        if not item:
            return None
        self.db.delete(item)
        self.db.commit()
        return item
