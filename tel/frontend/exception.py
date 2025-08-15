from nicegui import app, ui, Client
from fastapi import Request, Response

# --- 401 Page ---
@app.exception_handler(401)
async def exception_handler_401(request: Request, exception: Exception) -> Response:
    with Client(ui.page(''), request=request) as client:
        with ui.card(align_items='center').classes('absolute-center'):
            ui.label('Not authorized.')
            ui.link('Login', '/login')
    return client.build_response(request, 401)