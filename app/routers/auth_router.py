from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import AuthService
from app.database.connection import get_db
from app.security.jwt_handler import create_access_token
import traceback

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        return service.register_user(user.nombre, user.email, user.password, user.role)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        auth_user = service.authenticate_user(user.email, user.password)
        if not auth_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
        token = create_access_token({"sub": auth_user.email, "role": auth_user.role})
        print(f"Usuario logueado: {auth_user.email}, role: {auth_user.role}")
        return {"access_token": token}
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Error al autenticar usuario")
