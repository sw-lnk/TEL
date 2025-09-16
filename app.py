import os

from dotenv import load_dotenv
from nicegui import app, ui

from tel.database import init_database

from tel.authentification.router import router as auth_router
from tel.authentification.middleware import AuthMiddleware
from tel.user.router import router as user_router
from tel.frontend.router import router as ui_router
from tel.mission.router import router as mission_router

load_dotenv()

app.on_startup(init_database)

app.add_middleware(AuthMiddleware)

app.include_router(ui_router)
app.include_router(mission_router)
app.include_router(user_router)
app.include_router(auth_router)


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title='Technische Einsatzleitung',
        favicon='🚨',
        language="de-DE",
        dark=None,
        fastapi_docs=True,
        storage_secret=os.getenv("STORAGE_SECRET"),
        endpoint_documentation='page',
        reload=False,
    )
