from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlmodel import Field
from sqlmodel.main import SQLModel


from app.models.base import DBModel, Person, UpdatePerson


class Appointment(DBModel, table=True):
    date: datetime
    until: datetime
    description: Optional[str]
    doctor_id: int = Field(default=None, foreign_key="doctor.id")


class WorkingHours(DBModel, table=True):
    date: datetime
    until: datetime

    time_period_id: int = Field(default=None, foreign_key="timeperiod.id")


class TimePeriod(DBModel, table=True):
    date: datetime
    until: datetime

    doctor_id: int = Field(default=None, foreign_key="doctor.id")


class SpecialtyEnum(str, Enum):
    GENERAL_PRACTITIONER = "general practitioner"
    GYNECOLOGIST = "gynecologist"
    SURGEON = "surgeon"
    PEDIATRICIAN = "pediatrician"
    DERMATOLOGIST = "dermatologist"


class Specialty(DBModel, table=True):
    name: SpecialtyEnum
    
class DoctorSpecialtyLink(SQLModel, table=True):
    
    doctor_id: Optional[int] = Field(
        default=None, foreign_key="doctor.id", primary_key=True
    )
    
    specialty_id: Optional[int] = Field(
        default=None, foreign_key="specialty.id", primary_key=True
    )


class Doctor(Person, DBModel, table=True):
    pass

    # class Config:
    #     arbitrary_types_allowed = True
    #     json_encoders = {ObjectId: str}


class DoctorResponse(Person):
    schedule: List[TimePeriod] = []
    scheduled_appointments: List[Appointment] = []
    specialties: List[Specialty] = []


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
