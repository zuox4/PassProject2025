

from fastapi import APIRouter, HTTPException

from schemas.event import EventResponse, EventCreate, EventDelete, EventEdit
from utils import get_current_user
from schemas.user import User
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from models.event import Event, Eventer
from schemas.history_outs import Apcent
from models.apcents import ApcentModel
router = APIRouter(
    prefix="/api/apcents",
    tags=["Apcents"]

)


@router.put('/createapcent')
def create_apcent(data: Apcent, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    print(data)
    newApcent = ApcentModel(
        student_name=data.name,
        teacher_email=user.email,
        datetime=data.dateTime,
        class_name=data.className,
        cause=data.cause,
    )
    db.add(newApcent)
    db.commit()
    db.refresh(newApcent)
    return {'id': newApcent.id, 'name': newApcent.student_name, 'email': newApcent.teacher_email, 'datetime': newApcent.datetime, 'class_name': newApcent.class_name, 'cause': newApcent.cause}
