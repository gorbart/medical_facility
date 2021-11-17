from typing import List, Optional
from bson.objectid import ObjectId
from pydantic.main import BaseModel

from app.models.base import Person


class Patient(Person):
    disease_history: List[dict]
    medicine_taken: List[dict]
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}