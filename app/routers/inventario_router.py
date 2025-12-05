from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.services.inventario_service import InventarioService
from app.database.connection import get_db
from app.schemas.inventario_schema import InventarioCreate, InventarioResponse

router = APIRouter(prefix="/inventario", tags=["Inventario"])

@router.post("/", response_model=InventarioResponse)
def create_item(item: InventarioCreate, db: Session = Depends(get_db)):
    service = InventarioService(db)
    return service.create_item(item.dict())

@router.get("/", response_model=List[InventarioResponse])
def list_items(db: Session = Depends(get_db)):
    service = InventarioService(db)
    return service.get_all_items()

@router.get("/{codigo}", response_model=InventarioResponse)
def get_item(codigo: str, db: Session = Depends(get_db)):
    service = InventarioService(db)
    return service.get_item_by_codigo(codigo)

@router.put("/{inventario_id}")
def update_item(inventario_id: int, cantidad: int, db: Session = Depends(get_db)):
    service = InventarioService(db)
    return service.update_cantidad(inventario_id, cantidad)

@router.delete("/{inventario_id}")
def delete_item(inventario_id: int, db: Session = Depends(get_db)):
    service = InventarioService(db)
    return service.delete_item(inventario_id)
