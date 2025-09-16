from sqlmodel import select

from tel.database import get_session
from tel.mission.models import Mission, Status

def get_all_mission(archived: bool = False) -> list[Mission] | None:
    with get_session() as session:
        if archived:
            return session.exec(select(Mission)).all()
        return session.exec(select(Mission).where(Mission.status != Status.ARCHIVED)).all()

def get_mission(mission_label: str) -> Mission | None:
    with get_session() as session:
        return session.exec(select(Mission).where(Mission.label == mission_label)).first()