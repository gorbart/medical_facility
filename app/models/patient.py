from typing import List, Optional
from pydantic.main import BaseModel

from app.models.base import Person


class Patient(Person):
    disease_history: List[dict]
    medicine_taken: List[dict]