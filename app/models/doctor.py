from datetime import datetime
from typing import List, Optional, TypedDict

from bson.objectid import ObjectId

from app.models.base import Person, UpdatePerson


class Appointment(TypedDict):
    date: datetime
    until: datetime
    description: Optional[str]


class WorkingHours(TypedDict):
    date: datetime
    until: datetime


class TimePeriod(TypedDict):
    date: datetime
    until: datetime
    workingHours: List[WorkingHours]


class Doctor(Person):
    schedule: List[TimePeriod] = []
    scheduled_appointments: List[Appointment] = []
    specialities: List[str] = []

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateDoctor(UpdatePerson):
    """
    Model for updating Doctor data
    """
    schedule: Optional[List[TimePeriod]]
    scheduled_appointments: Optional[List[Appointment]]
    specialities: Optional[List[str]]

    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
