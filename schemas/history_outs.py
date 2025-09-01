from pydantic import BaseModel
from datetime import datetime


class CreatePass(BaseModel):
    name: str
    dateTime: datetime
    className: str
    comments: str


class Apcent(BaseModel):
    name:str
    dateTime: datetime
    className:str
    cause: str