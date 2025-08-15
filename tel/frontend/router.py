from nicegui import ui
from fastapi import APIRouter

from tel.frontend.pages.index import index_page
from tel.frontend.pages.login import login_page

router = APIRouter(tags=['Pages'])

# --- Landing Page ---
@ui.page('/', api_router=router)
async def index():
    await index_page()

@ui.page('/login', api_router=router)
async def login(redirect_to: str = '/'):
    await login_page(redirect_to)