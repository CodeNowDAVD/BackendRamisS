from fastapi import FastAPI
from app.routers.auth_router import router as auth_router
from app.database.base import Base
from app.database.connection import engine
from app.routers.rqs_router import router as rqs_router
from app.routers.rq_item_router import router as rq_item_router
from app.routers.orden_compra_router import router as orden_compra_router
from app.routers.inventario_router import router as inventario_router
# Importar modelos para crear tablas

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema con Roles y Auth")

# Incluir routers
app.include_router(auth_router)

app.include_router(rqs_router)
app.include_router(rq_item_router)
app.include_router(orden_compra_router)
app.include_router(inventario_router)