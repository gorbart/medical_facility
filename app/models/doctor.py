from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic.main import BaseModel
from sqlmodel import Field
from sqlmodel.main import Relationship, SQLModel

from app.models.base import DBModel, Person, UpdatePerson


class AppointmentInCreate(BaseModel):
    date: datetime
    until: datetime
    description: Optional[str]


class Appointment(DBModel, AppointmentInCreate, table=True):
    doctor_id: int = Field(default=None, foreign_key="doctor.id")


class WorkingHoursInCreate(BaseModel):
    date: datetime
    until: datetime


class WorkingHours(DBModel, WorkingHoursInCreate, table=True):
    time_period_id: int = Field(default=None, foreign_key="timeperiod.id")


class TimePeriodInCreate(BaseModel):
    date: datetime
    until: datetime

    working_hours: List[WorkingHoursInCreate]


class TimePeriodInResponse(BaseModel):
    date: datetime
    until: datetime

    working_hours: Optional[List[WorkingHoursInCreate]]


class TimePeriod(DBModel, table=True):
    date: datetime
    until: datetime

    doctor_id: int = Field(default=None, foreign_key="doctor.id")
    working_hours: List["WorkingHours"] = Relationship(
        sa_relationship_kwargs={"cascade": "all, delete"}
    )

class SpecialtyEnum(str, Enum):
    GENERAL_PRACTITIONER = "general_practitioner"
    GYNECOLOGIST = "gynecologist"
    SURGEON = "surgeon"
    PEDIATRICIAN = "pediatrician"
    DERMATOLOGIST = "dermatologist"


class DoctorSpecialtyLink(SQLModel, table=True):
    doctor_id: Optional[int] = Field(
        default=None, foreign_key="doctor.id", primary_key=True
    )

    specialty_id: Optional[int] = Field(
        default=None, foreign_key="specialty.id", primary_key=True
    )


class Specialty(DBModel, table=True):
    name: SpecialtyEnum
    doctors: List["Doctor"] = Relationship(back_populates="specialties", link_model=DoctorSpecialtyLink)


class Doctor(Person, DBModel, table=True):
    specialties: List["Specialty"] = Relationship(back_populates="doctors", link_model=DoctorSpecialtyLink)
    time_periods: List["TimePeriod"] = Relationship(
        sa_relationship_kwargs={"cascade": "all, delete"}
    )
    appointments: List["Appointment"] = Relationship(
        sa_relationship_kwargs={"cascade": "all, delete"}
    )

    # class Config:
    #     arbitrary_types_allowed = True
    #     json_encoders = {ObjectId: str}


class DoctorResponse(Person, DBModel):
    schedule: List[TimePeriodInCreate] = []
    scheduled_appointments: List[Appointment] = []
    specialties: List[Specialty] = []


class UpdateDoctor(UpdatePerson):
    """
    Model for updating Doctor data
    """
    pass

    # class Config:
    #     arbitrary_types_allowed = True
    #     allow_population_by_field_name = True
    #     json_encoders = {ObjectId: str}
