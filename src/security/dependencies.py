from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .security import decode_token, verify_password
from src.schemas.users import User, UserInDB
from src.database.queries.users import find_user


# Ruta donde se va a generar el token de acceso
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = decode_token(token)
        username = payload.get("sub")
        
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        user_dict = await find_user(username)
        if not user_dict:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado",
                headers={"WWW-Authenticate": "Bearer"}
            )
            
        return UserInDB(**user_dict)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error de autenticación: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"}
        )

    
async def authenticate_user(username: str, password: str):
    user_dict = await find_user(username)
    if not user_dict:
        return None
    
    user = UserInDB(**user_dict)
    
    if not verify_password(password, user.hashed_password):
        return None
        
    return user


async def check_owner(user: User = Depends(get_current_user)):
    if user.role != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes los permisos suficientes."
        )
    return user


async def check_manager(user: User = Depends(get_current_user)):
    if user.role != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes los permisos suficientes."
        )
    return user


async def check_employee(user: User = Depends(get_current_user)):
    if user.role != "employee":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes los permisos suficientes."
        )
    return user


async def check_employee_or_manager(user = Depends(get_current_user)):
    if user.role not in ["employee", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren privilegios de empleado o encargado"
        )
    return user


async def check_employee_or_owner(user = Depends(get_current_user)):
    if user.role not in ["employee", "owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren privilegios de empleado o dueño"
        )
    return user



async def check_manager_or_owner(user = Depends(get_current_user)):
    if user.role not in ["manager", "owner"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren privilegios de encargado o dueño"
        )
    return user