from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.services.rq_service import RQService
from app.database.connection import get_db
from app.schemas.rq_schema import RQCreate, RQResponse
from app.schemas.rq_estado_schema import RQEstadoUpdate
from app.schemas.rq_compra_schema import RQCompraEstadoResponse


router = APIRouter(prefix="/rqs", tags=["RQs"])

@router.post("/", response_model=RQResponse)
def create_rq(rq: RQCreate, db: Session = Depends(get_db)):
    service = RQService(db)
    try:
        return service.create_rq(rq.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[RQResponse])
def list_rqs(db: Session = Depends(get_db)):
    service = RQService(db)
    return service.get_all_rqs()

@router.get("/{rq_id}", response_model=RQResponse)
def get_rq(rq_id: int, db: Session = Depends(get_db)):
    service = RQService(db)
    try:
        return service.get_rq(rq_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{rq_id}/estado", response_model=RQResponse)
def update_rq_estado(rq_id: int, rq_estado: RQEstadoUpdate, db: Session = Depends(get_db)):
    service = RQService(db)
    try:
        return service.update_rq_estado(rq_id, rq_estado.estado)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{rq_id}")
def delete_rq(rq_id: int, db: Session = Depends(get_db)):
    service = RQService(db)
    try:
        service.delete_rq(rq_id)
        return {"detail": "RQ eliminada"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Endpoint para subir PDF y generar RQ automáticamente
@router.post("/upload_pdf", response_model=RQResponse)
def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Aquí se implementaría la lógica de pdfplumber o PyMuPDF
    # Extraer datos y crear RQ + items automáticamente
    service = RQService(db)
    rq_data = parse_pdf_to_rq(file)  # función que parsea PDF a diccionario
    return service.create_rq(rq_data)


@router.get("/{rq_id}/estado-compra", response_model=RQCompraEstadoResponse)
def ver_estado_compra(rq_id: int, db: Session = Depends(get_db)):
    service = RQService(db)
    try:
        return service.obtener_estado_compra(rq_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
