from nicegui import app, ui
from sqlmodel import select

from tel.database import get_session
from tel.user.models import User
from tel.authentification.utils import get_current_user, verify_password
from tel.authentification.router import store_user_token


async def login_user(username: str, password: str, redirect_to: str = '/') -> None:  # local function to avoid passing username and password as arguments
    with get_session() as session:
        user = session.exec(select(User).where(User.username == username)).first()
    
    if not user:
        ui.notify('Wrong username or password', color='negative')
    
    elif not user.is_active:
        ui.notify('Inactive user', color='warning')
        
    elif verify_password(password, user.hashed_password):
        await store_user_token(user)
        ui.navigate.to(redirect_to)  # go back to where the user wanted to go
    else:
        ui.notify('Wrong username or password', color='negative')

    return None


async def check_user_login(superuser: bool = False) -> bool:
    token = app.storage.user.get("access_token", False)
    if not token:
        return False
    
    user = await get_current_user(token)
    if not user:
        return False
    
    if superuser:
        return user.is_superuser
    
    return user.is_active
