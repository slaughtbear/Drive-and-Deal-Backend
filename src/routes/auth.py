from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.schemas.tokens import Token
from src.schemas.users import User
from src.security.dependencies import authenticate_user, check_owner
from src.security.security import create_access_token


auth = APIRouter()
    

@auth.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    '''
    Endpoint para iniciar sesión, se autentica el usuario mediante un nombre de usuario
    y una contraseña, retornando un token de acceso.
    '''
    # Se autentica el usuario mediante username y password recibidos en el frontend
    user = authenticate_user(form_data.username, form_data.password)

    if not user: # Si el nombre de usuario no se encuentra o la contraseña es incorrecta
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )
    
    access_token = create_access_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@auth.get("/owner/")
async def owner_route(current_user: User = Depends(check_owner)):
    return {'msg': f'Hola, {current_user.username}, bienvenido al panel de administrador para dueños.'}