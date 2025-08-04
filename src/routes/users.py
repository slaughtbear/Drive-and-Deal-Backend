from fastapi import APIRouter, HTTPException
from src.schemas.users import User, UserCreate
from src.database.queries.users import insert_user


users = APIRouter()


# @users.get("/")
# async def get_users():
#     return 'users list'


# @users.get("/{id}")
# async def get_user():
#     return 'user'


@users.post("/", response_model=User)
async def create_user(user_data: UserCreate) -> User:
    """Endpoint de tipo POST para registrar un usuario.

    Args:
        user_data (CarCreate): Datos del usuario que se desea registrar.

    Returns:
        response (Car): Usuario creado.
    """
    response = await insert_user(user_data.model_dump())
    if not response:
        raise HTTPException(
            status_code = 500, # internal server error
            detail = "Ocurrió un error inesperado. Por favor intente más tarde."
        )
    return response


# @users.put("/")
# async def update_user():
#     return 'updated user'


# @users.delete("/")
# async def delete_user():
#     return 'updated user'