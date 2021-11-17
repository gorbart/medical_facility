from datetime import datetime
from typing import Dict, List, Optional, Tuple

from bson.objectid import ObjectId
from app.models.base import DBModel, Person


class Doctor(Person, DBModel):
    schedule: List[Dict[Tuple[datetime, datetime], List[Tuple[datetime, datetime]]]]  
    scheduled_appointments: List[Tuple[datetime, datetime, Optional[str]]]
    specialities: List[dict]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}