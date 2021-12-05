from enum import IntEnum

from bson.objectid import ObjectId

from app.models.base import Person


class UserType(IntEnum):
    ADMIN = 0
    MANAGER = 1
    NURSE = 2


class User(Person):
    login: str
    password: str
    user_type: UserType
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
