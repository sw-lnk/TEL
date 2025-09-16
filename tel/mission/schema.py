from pydantic import BaseModel

from tel.mission.models import Status

class MissionStatusUpdate(BaseModel):
    label: str
    status: Status
