from datetime import datetime
from enum import Enum
from typing import List, Optional


from app.models.base import DBModel, Person, UpdatePerson


class Appointment(DBModel, table=True):
    date: datetime
    until: datetime
    description: Optional[str]


class WorkingHours(DBModel, table=True):
    date: datetime
    until: datetime


class TimePeriod(DBModel, table=True):
    date: datetime
    until: datetime
    workingHours: List[WorkingHours]
    
class SpecialtyEnum(str, Enum):
    GENERAL_PRACTITIONER = "general practitioner"
    GYNECOLOGIST = "gynecologist"
    SURGEON = "surgeon"
    PEDIATRICIAN = "pediatrician"
    DERMATOLOGIST = "dermatologist"

class Specialty(DBModel, table=True):
    name: SpecialtyEnum

class Doctor(Person, table=True):
    schedule: List[TimePeriod] = []
    scheduled_appointments: List[Appointment] = []
    specialties: List[Specialty] = []

    # class Config:
    #     arbitrary_types_allowed = True
    #     json_encoders = {ObjectId: str}


class UpdateDoctor(UpdatePerson):
    """
    Model for updating Doctor data
    """
    schedule: Optional[List[TimePeriod]]
    scheduled_appointments: Optional[List[Appointment]]
    specialties: Optional[List[str]]

    # class Config:
    #     arbitrary_types_allowed = True
    #     allow_population_by_field_name = True
    #     json_encoders = {ObjectId: str}
