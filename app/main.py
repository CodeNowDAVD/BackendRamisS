from fastapi import FastAPI
from app.routers.auth_router import router as auth_router
from app.database.base import Base
from app.database.connection import engine

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema con Roles y Auth")

# Incluir routers
app.include_router(auth_router)
