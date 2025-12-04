from fastapi import APIRouter

router = APIRouter(
    prefix="/example",
    tags=["Example"]
)

@router.get("/")
def example():
    return {"message": "Router funcionando correctamente!"}
