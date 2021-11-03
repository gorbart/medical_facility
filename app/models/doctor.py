from datetime import datetime
from typing import Dict, List, Optional, Tuple
from app.models.base import DBModel, Person


class Doctor(Person):
    schedule: List[Dict[Tuple[datetime, datetime], List[Tuple[datetime, datetime]]]]  
    scheduled_appointments: List[Tuple[datetime, datetime, Optional[str]]]
    specialities: List[dict]
