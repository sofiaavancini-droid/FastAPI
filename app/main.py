from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .import schemas, crud, models

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


from .utils import verify_password
from .auth import crear_token
from .deps import get_current_user, require_admin
from fastapi.security import OAuth2PasswordRequestForm

@app.post("/usuarios", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    try:
        return crud.crear_usuario(db, usuario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Buscamos al usuario por su email/username
    user = crud.obtener_usuario_por_email(db, form_data.username)
    
    # 2. Verificamos si existe y si la contraseña coincide
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
        
    # 3. Generamos el token JWT incluyendo el email y si es admin o no
    token = crear_token(sub=user.email, es_admin=user.es_admin)
    
    # 4. Devolvemos el token con la estructura del esquema schemas.Token
    return {"access_token": token, "token_type": "bearer"}

@app.get("/usuarios/me", response_model=schemas.UsuarioResponse)
def leer_perfil(current_user= Depends(get_current_user)):
    # Esta ruta está protegida, solo entra si mandas un token válido
    return current_user

@app.get("/admin/ping")
def admin_ping(admin= Depends(require_admin)):
    # Esta ruta está súper protegida, solo entra si el usuario tiene es_admin = True
    return {"ok": True, "role": "admin"}