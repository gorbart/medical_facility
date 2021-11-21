from datetime import datetime
from typing import Dict, List, Optional, Tuple, TypedDict

from bson.objectid import ObjectId
from app.models.base import Person


class Appointment(TypedDict):
    date:datetime
    until:datetime
    description:Optional[str]

class WorkingHours(TypedDict):
    date:datetime
    until:datetime

class TimePeriod(TypedDict):
    date:datetime
    until:datetime
    workingHours:List[WorkingHours]

class Doctor(Person):
    schedule: List[TimePeriod] = []
    scheduled_appointments: List[Appointment] = []
    specialities: List[str] = []
    

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
