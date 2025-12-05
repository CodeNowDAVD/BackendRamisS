# app/routers/ordenes_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.services.orden_compra_service import OrdenCompraService
from app.database.connection import get_db
from app.schemas.orden_compra_schema import OrdenCompraCreate, OrdenCompraSummaryResponse, OrdenCompraEntity, OrdenCompraResponse

router = APIRouter(prefix="/ordenes", tags=["Órdenes Parciales"])

@router.post("/", response_model=OrdenCompraSummaryResponse)
def create_orden(orden: OrdenCompraCreate, db: Session = Depends(get_db)):
    service = OrdenCompraService(db)
    try:
        return service.create_orden(orden.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/item/{rq_item_id}", response_model=List[OrdenCompraEntity])
def get_ordenes(rq_item_id: int, db: Session = Depends(get_db)):
    service = OrdenCompraService(db)
    return service.get_ordenes_by_item(rq_item_id)

@router.put("/{orden_id}", response_model=OrdenCompraEntity)
def update_orden(orden_id: int, db: Session = Depends(get_db), **kwargs):
    service = OrdenCompraService(db)
    try:
        return service.update_orden(orden_id, **kwargs)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
from fastapi import Body

@router.patch("/{orden_id}/editar")
def editar_orden(orden_id: int, cambios: dict = Body(...), db: Session = Depends(get_db)):
    service = OrdenCompraService(db)
    try:
        return service.patch_orden(orden_id, cambios)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/resumen")
def resumen_ordenes(db: Session = Depends(get_db)):
    """
    Retorna todas las órdenes de compra agrupadas por RQ,
    con el progreso, exceso y estado de cada ítem.
    """
    service = OrdenCompraService(db)
    try:
        return service.listar_ordenes_por_rq()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.delete("/{orden_id}")
def delete_orden(orden_id: int, db: Session = Depends(get_db)):
    service = OrdenCompraService(db)
    try:
        return service.delete_orden(orden_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
