from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from tel.database import get_session
from tel.user.models import User
from tel.mission.models import Mission, MissionDetail, MissionNew, Status, Message, MessageList
from tel.authentification.utils import get_current_active_user

router = APIRouter(prefix='/mission', tags=['Mission'])


@router.get('/all', response_model=list[Mission])
async def get_all_mission(current_user: Annotated[User, Depends(get_current_active_user)]):
    with get_session() as session:
        return session.exec(select(Mission)).all()


@router.get('/{mission_label}', response_model=MissionDetail)
async def get_mission_details(mission_label: str, current_user: Annotated[User, Depends(get_current_active_user)]):
    with get_session() as session:
        mission = session.exec(select(Mission).where(Mission.label == mission_label)).first()

        if not mission:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail=f'Found no mission with lable "{mission_label}"'
            )

        return mission
    

@router.get('/{mission_label}/messages', response_model=list[MessageList])
async def get_mission_messages(mission_label: str, current_user: Annotated[User, Depends(get_current_active_user)]):
    with get_session() as session:
        mission = session.exec(select(Mission).where(Mission.label == mission_label)).first()
        return mission.messages
    
    
@router.post('/new', response_model=Mission)
async def create_mission(new_mission: MissionNew, current_user: Annotated[User, Depends(get_current_active_user)]):
    mission = Mission.model_validate(new_mission)
    with get_session() as session:
        session.add(mission)
        session.commit()
        session.refresh(mission)
        return mission


@router.put('/statusupdate')
async def set_status(label: str, new_status: Status, current_user: Annotated[User, Depends(get_current_active_user)]):
    with get_session() as session:
        mission = session.exec(select(Mission).where(Mission.label == label)).first()
        
        if not mission:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f'Found no mission with lable "{label}"')

        mission.status = new_status
        session.add(mission)
        session.commit()
        session.refresh(mission)
        return mission


@router.post('/message', response_model=Message)
async def add_message(mission_label: str, content: str, current_user: Annotated[User, Depends(get_current_active_user)]):
    with get_session() as session:
        mission = session.exec(select(Mission).where(Mission.label == mission_label)).first()
        
        if not mission:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f'Found no mission with lable "{mission_label}"')
        
        message = Message(
            mission_id=mission.id,
            content=content,
            user_id=current_user.id
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message
