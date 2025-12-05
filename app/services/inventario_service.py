from sqlalchemy.orm import Session
from app.repositories.inventario_repository import InventarioRepository
from app.models.inventario_model import Inventario

class InventarioService:
    def __init__(self, db: Session):
        self.repo = InventarioRepository(db)

    def create_item(self, item_data: dict):
        item = Inventario(**item_data)
        return self.repo.create(item)

    def get_item_by_codigo(self, codigo: str):
        return self.repo.get_by_codigo(codigo)

    def get_all_items(self):
        return self.repo.get_all()

    def update_cantidad(self, inventario_id: int, cantidad: int):
        return self.repo.update_cantidad(inventario_id, cantidad)

    def delete_item(self, inventario_id: int):
        return self.repo.delete(inventario_id)
