from dotenv import load_dotenv
import os

load_dotenv()
BASE_UPLOAD_DIR = os.path.join(os.getcwd(), "uploads", "ordenes_compra")
os.makedirs(BASE_UPLOAD_DIR, exist_ok=True)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
DATABASE_URL = os.getenv("DATABASE_URL")
