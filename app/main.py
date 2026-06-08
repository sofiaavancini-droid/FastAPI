from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import schemas, crud, models


from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/productos", response_model=list[schemas.ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return crud.obtener_productos(db)


@app.post("/productos", response_model=schemas.ProductoResponse)
def agregar_producto(
    producto: schemas.ProductoCreate,
    db: Session = Depends(get_db)
):
    return crud.crear_producto(db, producto)


@app.put("/productos/{producto_id}",
         response_model=schemas.ProductoResponse)
def actualizar_producto(
    producto_id: int,
    producto: schemas.ProductoCreate,
    db: Session = Depends(get_db)
):
    producto_actualizado = crud.actualizar_producto(
        db,
        producto_id,
        producto
    )

    if not producto_actualizado:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return producto_actualizado


@app.delete("/productos/{producto_id}")
def eliminar_producto(
    producto_id: int,
    db: Session = Depends(get_db)
):
    producto_eliminado = crud.eliminar_producto(
        db,
        producto_id
    )

    if not producto_eliminado:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return {"mensaje": "Producto eliminado"}