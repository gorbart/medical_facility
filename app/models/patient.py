from typing import List, Optional
from bson.objectid import ObjectId
from datetime import datetime
from typing_extensions import TypedDict

from app.models.base import DBModel, Person, UpdatePerson


class Medicine(DBModel, table=True):
    name: str
    until: datetime


class MedicinesTaken(DBModel, table=True):
    date: datetime
    medicines: List[Medicine]


class Patient(Person, table=True):
    
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
    disease_history: Optional[List[dict]]

    medicine_taken: Optional[List[MedicinesTaken]]

    # class Config:
    #     arbitrary_types_allowed = True
    #     allow_population_by_field_name = True
    #     json_encoders = {ObjectId: str}
