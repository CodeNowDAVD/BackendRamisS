from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.core.security import hash_password, verify_password

class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def register_user(self, nombre: str, email: str, password: str, role: str = "user"):
        if self.user_repo.get_by_email(email):
            raise ValueError("User already exists")
        hashed_password = hash_password(password)
        user = User(nombre=nombre, email=email, password=hashed_password, role=role)
        return self.user_repo.create_user(user)

    def authenticate_user(self, email: str, password: str):
        user = self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password):
            return None
        return user
