
import datetime
from fastapi import APIRouter, HTTPException

import find_user
import studentsDB
from schemas.classes import AddPermission
from schemas.event import EventResponse, EventCreate, EventDelete, EventEdit
from utils import get_current_user
from schemas.user import User
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from models.event import Event, Eventer
from models.classes import ClassPermission
from schemas.classes import AddPermission
from models.classes import ClassPermission
from models.apcents import ApcentModel
from sqlalchemy import cast, Date
router = APIRouter(
    prefix="/api/classes",
    tags=['ClassesDashboard']
)


@router.get('/myClasses')
def get_my_classes(db: Session = Depends(get_db), user: User = Depends(get_current_user)):


    user_email = user.email
    my_classes = find_user.find_user(user_email).get('classes')
    permission_classes = db.query(ClassPermission).filter(ClassPermission.class_menagers_email == user_email).all()
    today = datetime.datetime.now().date()
    today_start = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + datetime.timedelta(days=1)
    data1 = []

    for name in my_classes:
        permission = db.query(ClassPermission).filter(
            ClassPermission.class_name == name
        ).first()
        apcents = [
            i.student_name
            for i in db.query(ApcentModel)
            .filter(ApcentModel.datetime >= today_start)
            .filter(ApcentModel.datetime < today_end)
            .filter(ApcentModel.class_name == name)
            .all()
        ]

        data1.append({
            'name': name,
            'permission_teacher': permission.class_menagers_email if permission else '',
            'students': studentsDB.get_class_from_db(class_name=name),
            'apcents': apcents
        })
    print(data1)
    if permission_classes:
        data2 = [{'name': i.class_name, 'students': studentsDB.get_class_from_db(class_name=i.class_name), 'apcents': [i.student_name for i in db.query(ApcentModel).filter(ApcentModel.class_name==i.class_name).filter(ApcentModel.datetime >= today_start)
            .filter(ApcentModel.datetime < today_end).all()] } for i in permission_classes]
    else:
        data2 = []
    data = {
        "my_classes": data1,
        "permission_classes":
            data2
    }
    return data


@router.post('/add-permission')
def get_my_classes(data: AddPermission, db: Session = Depends(get_db), user: User = Depends(get_current_user)):

    permission = db.query(ClassPermission).filter(ClassPermission.class_name == data.groupName).all()
    if len(permission) > 0:
        for permission in permission:
            db.delete(permission)
    newPermission = ClassPermission(
            class_name=data.groupName,
            class_menagers_email=data.permission_teacher
        )
    db.add(newPermission)
    db.commit()
    return {'name': newPermission.class_name, 'email': newPermission.class_menagers_email}


@router.post('/del-permission/{className}')
def get_my_classes(className: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    permission = db.query(ClassPermission).filter(ClassPermission.class_name == className).first()
    db.delete(permission)
    db.commit()
    return className

