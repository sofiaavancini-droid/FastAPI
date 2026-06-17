from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


import app.crud as crud
import app.schemas as schemas
from app.deps.deps import get_db  

router = APIRouter()


@router.get("/", response_model=list[schemas.CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    return crud.obtener_categorias(db)


@router.post("/", response_model=schemas.CategoriaResponse)
def crear_categoria(
    categoria: schemas.CategoriaCreate,
    db: Session = Depends(get_db)
):
    return crud.crear_categoria(db, categoria)