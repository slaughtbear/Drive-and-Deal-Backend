from fastapi import APIRouter, HTTPException
from src.schemas.users import User, UserCreate
from src.database.queries.users import find_user, insert_user
from src.security.security import get_hashed_password


users = APIRouter()


@users.post("/", response_model=User)
async def create_user(user_data: UserCreate) -> User:
    # Verificar que las contraseñas coincidan
    if user_data.password != user_data.password_confirm:
        raise HTTPException(
            status_code=400,
            detail="Las contraseñas no coinciden"
        )
    
    # Verificar si el usuario ya existe
    existing_user = await find_user(user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="El nombre de usuario ya está en uso"
        )
    
    # Hashear la contraseña
    hashed_password = get_hashed_password(user_data.password)
    
    # Crear el diccionario de usuario
    user_dict = user_data.model_dump(exclude={"password", "password_confirm"})
    user_dict["hashed_password"] = hashed_password
    user_dict["disabled"] = False
    
    response = await insert_user(user_dict)
    if not response:
        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error inesperado. Por favor intente más tarde."
        )
    return response