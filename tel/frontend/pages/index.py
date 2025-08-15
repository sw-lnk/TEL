from nicegui import ui

from tel.frontend.utils import check_user_login
from tel.frontend.theme import frame
from tel.authentification.router import clear_user_data

async def index_page():
    async def logout():
        await clear_user_data()
        ui.navigate.to('/login')
        
    with frame():
        with ui.card(align_items='center').classes('absolute-center'):
            ui.label("Technische Einsatzleitung").classes('text-2xl')
            
            if await check_user_login():
                ui.button('Logout', on_click=logout)
            else:
                ui.button('Login', on_click=lambda: ui.navigate.to('/login'))
    
    return None