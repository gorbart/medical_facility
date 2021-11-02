from datetime import datetime
from typing import List, Optional, Tuple
from app.models.base import DBModel, Person


class Doctor(Person):
    availabilites: List[List[Tuple[datetime, datetime]]]  
    scheduled_appointments: List[Tuple[datetime, datetime, Optional[str]]]
    specialities: List[dict]
