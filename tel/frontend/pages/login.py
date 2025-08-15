from typing import Optional

from nicegui import ui
from fastapi.responses import RedirectResponse

from tel.frontend.theme import frame, menu
from tel.frontend.utils import check_user_login, login_user


async def login_page(redirect_to: str = '/') -> Optional[RedirectResponse]:
    async def login() -> None:
        if await login_user(username.value, password.value, redirect_to):
            menu.refresh()
        
    if await check_user_login():
        return RedirectResponse('/')
    
    with frame():
        with ui.card().classes('absolute-center'):
            username = ui.input('Username').on('keydown.enter', login)
            password = ui.input('Password', password=True, password_toggle_button=True).on('keydown.enter', login)
            ui.button('Log in', on_click=login)
    return None