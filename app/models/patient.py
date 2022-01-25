from typing import List, Optional
from bson.objectid import ObjectId
from datetime import date, datetime
from typing_extensions import TypedDict
from pydantic.main import BaseModel
from sqlmodel import Relationship

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
    medicines: List["Medicine"] = Relationship(
        sa_relationship_kwargs={"cascade": "all, delete"}
    )
    
class MedicinesTakenInResponse(BaseModel):
    id: int
    date: datetime
    medicines: List[Medicine]

    def to_dict(self):
        return {"id": self.id, "date": str(self.date), "medicines": [medicine.as_dict() for medicine in self.medicines]}


class MedicinesTakenInCreate(BaseModel):
    date: datetime
    medicines: List[dict]


class Disease(DBModel, table=True):
    date: datetime
    name: str

    patient_id: int = Field(default=None, foreign_key="patient.id")


class Patient(Person, DBModel, table=True):

    diseases: List["Disease"] = Relationship(
        sa_relationship_kwargs={"cascade": "all, delete"}
    )
    
    medicines_taken: List["MedicinesTaken"] = Relationship(
        sa_relationship_kwargs={"cascade": "all, delete"}
    )
    # class Config:
    #     arbitrary_types_allowed = True
    #     allow_population_by_field_name = True
    #     json_encoders = {ObjectId: str}


class PatientInResponse(Person):
    disease_history: List[dict] = []
    medicine_taken: List[dict] = []

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
