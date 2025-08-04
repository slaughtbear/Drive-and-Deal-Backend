from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .security import decode_token, verify_password
from src.schemas.users import User
from src.database.queries.users import find_user


# Ruta donde se va a generar el token de acceso
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    '''
    A partir del JWT enviado por el cliente
    '''
    payload = decode_token(token) # Se decodifica el token del header en la petición
    username = payload.get("sub") # Obtiene el nombre de usuario del identificador del token ("sub")

    if username is None: # Si no se obtiene ningún nombre de usuario
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
    # Si se obtiene un nombre de usuario, se procede a buscarlo en la base de datos
    user = find_user(username) 

    # Si no se encuentra el usuario en la base de datos
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )
    
    return user # Devuelve el usuario almacenado en la base de datos

    
def authenticate_user(username: str, password: str):
    user = find_user(username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def check_owner(user: User = Depends(get_current_user)):
    if user.role != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes los permisos suficientes."
        )
    return user


def check_manager(user: User = Depends(get_current_user)):
    if user.role != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes los permisos suficientes."
        )
    return user


def check_employee(user: User = Depends(get_current_user)):
    if user.role != "employee":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes los permisos suficientes."
        )
    return user