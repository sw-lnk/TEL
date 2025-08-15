from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from nicegui import app

from tel.authentification.utils import get_current_user

from tel.authentification.constants import unrestricted_page_routes


class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        token: str = app.storage.user.get("access_token")
        if token:
            if not await get_current_user(token):
                return RedirectResponse(f'/login?redirect_to={request.url.path}')
        
        else:            
            if not request.url.path.startswith('/_nicegui') and request.url.path not in unrestricted_page_routes:
                return RedirectResponse(f'/login?redirect_to={request.url.path}')
        
        return await call_next(request)
