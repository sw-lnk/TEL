from enum import Enum
import os
from sqlmodel import SQLModel, Field, Relationship
from dotenv import load_dotenv
from datetime import datetime

from tel.user.models import User

load_dotenv()

class Status(str, Enum):
    NEW = 'Neu'
    IN_WORK = 'In arbeit'
    FINISHED = 'Abgeschlossen'
    ARCHIVED = 'Archiviert'


class MissionNew(SQLModel):
    label: str = Field(unique=True)
    street: str
    zip_code: int = os.getenv('ZIP_CODE')
    status: Status = Status.NEW


class MissionDetail(MissionNew):
    pass


class Mission(MissionNew, table=True):    
    id: int | None = Field(default=None, primary_key=True, index=True)
    
    messages: list["Message"] = Relationship(back_populates="mission")


class MessageList(SQLModel):
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    
    
class Message(MessageList, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    
    mission_id: int = Field(default=None, foreign_key="mission.id")
    mission: Mission | None = Relationship(back_populates="messages")
    
    user_id: int = Field(default=None, foreign_key="user.id")
    user: User | None = Relationship(back_populates="messages")
    
    
