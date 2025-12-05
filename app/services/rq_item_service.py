from sqlalchemy.orm import Session
from app.repositories.rq_item_repository import RQItemRepository
from app.models.rq_item_model import RQItem

class RQItemService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = RQItemRepository(db)

    def create_item(self, item_data: dict, rq_id: int):
        item = RQItem(
            codigo=item_data["codigo"],
            descripcion=item_data["descripcion"],
            cantidad=item_data["cantidad"],
            unidad=item_data["unidad"],
            rq_id=rq_id
        )
        return self.repo.create(item)

    def get_items_by_rq(self, rq_id: int):
        return self.repo.get_by_rq(rq_id)

    def update_estado(self, item_id: int, estado: str):
        return self.repo.update_estado(item_id, estado)

    def delete_item(self, item_id: int):
        return self.repo.delete(item_id)
