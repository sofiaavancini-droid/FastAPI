from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .auth import verificar_token
from .import crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autenticado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verificar_token(token)
    if payload is None:
        raise cred_exc
        
    email: str | None = payload.get("sub")
    if email is None:
        raise cred_exc
        
    user = crud.obtener_usuario_por_email(db, email)
    if user is None:
        raise cred_exc
        
    return user

def require_admin(current_user= Depends(get_current_user)):
    if not current_user.es_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="No autorizado: se requiere rol admin"
        )
    return current_user