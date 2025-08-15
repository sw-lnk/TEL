from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from pydantic import SecretStr

from tel.database import get_session
from tel.user.models import User, UserBase, UserProfile
from tel.user.schemas import UserUpdate
from tel.authentification.utils import get_current_active_user, get_current_super_user, get_password_hash


router = APIRouter(prefix='/user', tags=['User'])

@router.get('/all', response_model=list[UserBase])
async def get_all_user(current_user: Annotated[User, Depends(get_current_super_user)]):
    with get_session() as session:
        return session.exec(select(User)).all()
    

@router.get("/me", response_model=UserProfile)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.put("/me/password")
async def change_my_password(
    current_user: Annotated[User, Depends(get_current_active_user)],
    password: SecretStr,
    password_conformation: SecretStr,
):
    if password != password_conformation:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Check new password.")
    
    with get_session() as session:
        user = session.exec(select(User).where(User.username == current_user.username)).first()
        user.hashed_password = get_password_hash(password.get_secret_value())
        session.commit()
        session.refresh(user)
        return {'message': f'Password for user {user.username} changed successful.'}


@router.get("/{username}", response_model=UserProfile)
async def show_users_profile(
    username: str,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    with get_session() as session:
        user = session.exec(select(User).where(User.username == username)).first()
        
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User '{username}' not known")
        
        return user


@router.put("/{username}", response_model=UserProfile)
async def update_users_profile(
    username: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    user_data: UserUpdate
):
    if not user_data.model_dump(exclude_none=True):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No data provided")
    
    if (username == current_user.username) or current_user.is_superuser:            
        with get_session() as session:
            user = session.exec(select(User).where(User.username == username)).first()
            
            if not user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User '{username}' not known")
            
            if user_data.username:
                user.username = user_data.username
            
            if user_data.email:
                user.email = user_data.email
            
            if user_data.is_active:
                user.is_active = user_data.is_active
            
            if user_data.is_active:
                user.is_superuser = user_data.is_superuser
            
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Insufficent permissions')    
