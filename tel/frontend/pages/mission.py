from nicegui import ui

from tel.frontend.theme import frame
from tel.mission.utils import get_mission, get_all_mission

async def mission_all(archived: bool = False):
    missions =  get_all_mission(archived)
    
    with frame("Einsatzübersicht"):
        for mission in missions:
            with ui.row():
                ui.label(f"Einsatznr.: {mission.label} - {mission.street} [{mission.status.name}]")
    
    return None


async def mission_details(mission_label: str):
    mission = get_mission(mission_label)

    with frame():
        with ui.card(align_items='center').classes('absolute-center'):
            if mission:           
                ui.label(f"Einsatznr.: {mission.label}").classes('text-2xl')
                ui.label(mission.street)
            else:
                ui.label(f"Einsatznr. {mission_label} nicht bekannt.").classes('text-2xl')
    
    return None
