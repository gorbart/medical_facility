from datetime import datetime
from typing import List, Optional, Dict, Tuple
from bson.objectid import ObjectId
from pydantic.main import BaseModel

from app.models.base import Person


class Patient(Person):
    disease_history: List[dict]

    #medicine_taken: List[dict]
    medicine_taken: List[Dict[datetime, Tuple[str, datetime, datetime]]]
    
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: lambda v: str(v)}