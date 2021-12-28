from typing import List, Optional
from bson.objectid import ObjectId
from datetime import datetime
from typing_extensions import TypedDict
from pydantic.main import BaseModel

from sqlmodel.main import Field

from app.models.base import DBModel, Person, UpdatePerson


class Medicine(DBModel, table=True):
    name: str
    until: datetime

    medicines_taken_id: int = Field(
        default=None, foreign_key="medicinestaken.id")


class MedicinesTaken(DBModel, table=True):
    date: datetime

    patient_id: int = Field(default=None, foreign_key="patient.id")


class MedicinesTakenInCreate(BaseModel):
    date: datetime
    medicines: List[dict]


class Disease(DBModel, table=True):
    date: datetime
    name: str

    patient_id: int = Field(default=None, foreign_key="patient.id")


class Patient(Person, DBModel, table=True):

    pass
    # class Config:
    #     arbitrary_types_allowed = True
    #     allow_population_by_field_name = True
    #     json_encoders = {ObjectId: str}


class PatientResponse(Person):

    disease_history: List[dict] = []
    medicine_taken: List[MedicinesTaken] = []

    # class Config:
    #     arbitrary_types_allowed = True
    #     allow_population_by_field_name = True
    #     json_encoders = {ObjectId: str}


class UpdatePatient(UpdatePerson):
    """
    Model for updating Patient data
    """

    pass
    # class Config:
    #     arbitrary_types_allowed = True
    #     allow_population_by_field_name = True
    #     json_encoders = {ObjectId: str}
