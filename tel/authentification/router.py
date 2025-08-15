from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from nicegui import app
from pydantic import ValidationError

from tel.user.models import User
from tel.user.schemas import UserRegister
from tel.authentification.utils import authenticate_user, get_password_hash, create_access_token, get_current_active_user, get_current_super_user
from tel.authentification.schemas import Token
from tel.authentification.constants import URL_PREFIX_AUTH, ACCESS_TOKEN_EXPIRE_MINUTES
from tel.database import get_session


router = APIRouter(prefix=f'/{URL_PREFIX_AUTH}', tags=['Authentification'])


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    token = Token(access_token=access_token)    
    return token


@router.post('/register', response_model=User)
async def create_new_user(new_user: UserRegister, current_user: Annotated[User, Depends(get_current_super_user)]):
    with get_session() as session:
        user = User(
            username=new_user.username,
            email=new_user.email,
            hashed_password=get_password_hash(new_user.password.get_secret_value())
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@router.put('/storetoken')
async def store_user_token(current_user: Annotated[User, Depends(get_current_active_user)]):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.username}, expires_delta=access_token_expires
    )    
    token = Token(access_token=access_token)
    app.storage.user.update(token.model_dump())
    app.storage.user.update({'username': current_user.username})
    return {'message': 'Token stored'}


@router.get('/readtoken', response_model=Token)
async def get_user_token(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    try:
        return Token(access_token=app.storage.user.get("access_token"),
                    token_type=app.storage.user.get("token_type")
                )
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get('/userdata')
async def get_user_data():
    return app.storage.user


@router.delete('/clear')
async def clear_user_data():
    app.storage.user.clear()
    return {'message': 'Cleared user data'}
