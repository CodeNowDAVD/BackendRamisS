# app/services/pdf_import_service.py
import pdfplumber
import re
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.rq_model import Requerimiento
from app.models.rq_item_model import RQItem

class PDFImportService:
    def __init__(self, db: Session):
        self.db = db

    def parse_rq_pdf(self, pdf_path: str):
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"

        # Extraer número de RQ y fecha
        nro_rq_match = re.search(r"NRO-(\d+)", text)
        fecha_match = re.search(r"Fecha Emisión\s*:\s*(\d{2}/\d{2}/\d{4})", text)

        nro_rq = nro_rq_match.group(1) if nro_rq_match else None
        fecha_emision = datetime.strptime(fecha_match.group(1), "%d/%m/%Y") if fecha_match else datetime.utcnow()

        # Extraer proyecto y solicitante (aprox)
        proyecto_match = re.search(r"Zona o Proyecto\s*:\s*(.*?)\s*Fecha Emisión", text)
        solicitante_match = re.search(r"Solicitado Por\s*:\s*(.*?)\n", text)
        proyecto = proyecto_match.group(1).strip() if proyecto_match else "Desconocido"
        solicitante = solicitante_match.group(1).strip() if solicitante_match else "Desconocido"

        # Extraer ítems
        items = []
        items_text = text.split("ÍTEM CÓDIGO DESCRIPCIÓN")[-1]
        lines = items_text.strip().split("\n")

        for line in lines:
            item_match = re.match(r"\d+\s+(\w+)\s+(.*?)\s+\S+\s+([\d.]+)\s+(\S+)", line)
            if item_match:
                codigo, descripcion, cantidad, unidad = item_match.groups()
                items.append({
                    "codigo": codigo.strip(),
                    "descripcion": descripcion.strip(),
                    "cantidad": float(cantidad),
                    "unidad": unidad.strip()
                })

        return {
            "nro_rq": nro_rq,
            "fecha_emision": fecha_emision,
            "proyecto": proyecto,
            "solicitante": solicitante,
            "items": items
        }

    def crear_requerimiento_desde_pdf(self, pdf_path: str):
        data = self.parse_rq_pdf(pdf_path)
        if not data["nro_rq"]:
            raise ValueError("No se pudo extraer el número de RQ")

        # Crear Requerimiento
        rq = Requerimiento(
            nro_rq=f"NRO-{data['nro_rq']}",
            proyecto=data["proyecto"],
            solicitante=data["solicitante"],
            fecha_emision=data["fecha_emision"]
        )
        self.db.add(rq)
        self.db.commit()
        self.db.refresh(rq)

        # Crear ítems
        for item_data in data["items"]:
            rq_item = RQItem(
                rq_id=rq.id,
                codigo=item_data["codigo"],
                descripcion=item_data["descripcion"],
                cantidad=item_data["cantidad"],
                unidad=item_data["unidad"]
            )
            self.db.add(rq_item)
        self.db.commit()

        return {
            "message": f"Requerimiento {rq.nro_rq} importado con {len(data['items'])} ítems",
            "rq_id": rq.id
        }
