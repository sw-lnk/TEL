from nicegui import ui
from fastapi import APIRouter

from tel.frontend.pages.index import index_page
from tel.frontend.pages.login import login_page
from tel.frontend.pages.mission import mission_details, mission_all

router = APIRouter(tags=['Pages'])

# --- Landing Page ---
@ui.page('/', api_router=router)
async def index():
    await index_page()

@ui.page('/login', api_router=router)
async def login(redirect_to: str = '/'):
    await login_page(redirect_to)

@ui.page('/einsatz', api_router=router)
async def mission_list():
    await mission_all()
    
@ui.page('/einsatz/{mission_label}', api_router=router)
async def mission_detail(mission_label: str):
    await mission_details(mission_label)