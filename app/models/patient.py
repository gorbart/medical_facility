from typing import List, TypedDict
from bson.objectid import ObjectId
from datetime import datetime

from app.models.base import Person


class Medicines(TypedDict):
    name: str
    until: datetime


class MedicinesTaken(TypedDict):
    date: datetime
    medicines: List[Medicines]


class Patient(Person):
    disease_history: List[dict] = []

    medicine_taken: List[MedicinesTaken] = []
    
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
