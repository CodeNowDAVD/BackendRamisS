from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles  # Importante para ver los archivos
import os

from app.database.base import Base
from app.database.connection import engine

# Importar tus routers existentes
from app.routers.auth_router import router as auth_router
from app.routers.rqs_router import router as rqs_router
from app.routers.rq_item_router import router as rq_item_router
from app.routers.orden_compra_router import router as orden_compra_router
from app.routers.inventario_router import router as inventario_router
from app.routers.pdf_import_router import router as importar_rq
from app.routers.upload_router import router as upload_router
from app.routers.comprobantes_router import router as comprobantes_router

# Nuevo Router de Requerimientos Mobile
from app.routers.rq_personalizado_router import router as rq_personalizado_router


# -------------------------------
# CREAR TABLAS
# -------------------------------
Base.metadata.create_all(bind=engine)


# -------------------------------
# APP
# -------------------------------
app = FastAPI(title="Sistema con Roles y Auth")


# -------------------------------
# CREACIÓN AUTOMÁTICA DE CARPETAS
# (NO toca templates, solo asegura existencia)
# -------------------------------
FOLDERS = [
    "uploads",
    "uploads/comprobantes",
    "uploads/ordenes_compra",

    "temp_files",

    "static",
    "static/firmas",
    "static/generados",
    "static/templates"  # 👈 ESTA SE SUBE A GITHUB (plantillas)
]

for folder in FOLDERS:
    os.makedirs(folder, exist_ok=True)


# -------------------------------
# ARCHIVOS ESTÁTICOS
# -------------------------------
# Permite acceder a:
# http://tu-dominio/static/generados/archivo.xlsx
app.mount("/static", StaticFiles(directory="static"), name="static")


# -------------------------------
# ROUTERS
# -------------------------------
app.include_router(comprobantes_router)
app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(inventario_router)
app.include_router(importar_rq)
app.include_router(rqs_router)
app.include_router(rq_item_router)
app.include_router(orden_compra_router)
app.include_router(rq_personalizado_router)  # Integrado
