from enum import Enum

from bson.objectid import ObjectId

from app.models.base import Person


class UserType(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    NURSE = "nurse"


class User(Person):
    login: str
    password: str
    user_type: UserType
    
    # class Config:
    #     arbitrary_types_allowed = True
    #     json_encoders = {ObjectId: str}
