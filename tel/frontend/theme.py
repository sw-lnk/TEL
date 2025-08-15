from contextlib import contextmanager

from nicegui import ui


def menu() -> None:
    ui.link('Home', '/').classes(replace='text-white')
    ui.link('Docs', '/docs').classes(replace='text-white')    
    ui.link('Login', '/login').classes(replace='text-white')


@contextmanager
def frame(navigation_title: str = None):
    """Custom page frame to share the same styling and behavior across all pages"""
    ui.colors(primary='#6E93D6', secondary='#53B689', accent='#111B1E', positive='#53B689')
    with ui.header():
        ui.label('TEL').classes('font-bold')
        ui.space()
        if navigation_title:
            ui.label(navigation_title)
            ui.space()
        with ui.row():
            menu()
    with ui.column():
        yield