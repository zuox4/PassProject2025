

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
from schemas.history_outs import DeleteApcentRequest
import datetime
from studentsDB import get_all_classes
from fastapi import Query, HTTPException
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


@router.delete('/deleteapcent')
def delete_apcents(data: DeleteApcentRequest,db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    apcent = db.query(ApcentModel).filter(ApcentModel.student_name == data.name, ApcentModel.class_name==data.className).first()
    db.delete(apcent)
    db.commit()

    print(data)
    return {'id': data}


@router.get('/allapcents')
def get_apcents(
        date: str = Query(None, description="Дата в формате YYYY-MM-DD"),
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    # Если дата не указана в запросе, используем сегодняшнюю дату
    if date:
        try:
            # Парсим дату из запроса
            requested_date = datetime.datetime.strptime(date, "%Y-%m-%d")
            today_start = requested_date.replace(hour=0, minute=0, second=0, microsecond=0)
        except ValueError:
            raise HTTPException(status_code=400, detail="Неверный формат даты. Используйте YYYY-MM-DD")
    else:
        # Если дата не указана, используем сегодня
        today_start = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    today_end = today_start + datetime.timedelta(days=1)

    all_classes = get_all_classes()
    apcents = db.query(ApcentModel).filter(
        ApcentModel.datetime >= today_start,
        ApcentModel.datetime < today_end
    ).all()

    group = {}

    # Сначала инициализируем все классы
    for class_name, total_count in all_classes.items():
        group[class_name] = {"total": total_count, "apcents": []}

    # Затем добавляем апценты
    for apcent in apcents:
        if apcent.class_name in group:
            group[apcent.class_name]["apcents"].append({
                "student_name": apcent.student_name,
                "datetime": apcent.datetime,
                "cause": apcent.cause,
            })

    return {'apcents': group}




