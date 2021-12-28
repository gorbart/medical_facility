import enum
from bson.objectid import ObjectId
from sqlmodel import Field, Column, Enum

from app.models.base import DBModel, Person


class UserType(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    NURSE = "nurse"


class User(Person, DBModel, table=True):
    login: str
    password: str
    user_type: UserType = Field(sa_column=Column(Enum(UserType)))
    
    # class Config:
    #     arbitrary_types_allowed = True
    #     json_encoders = {ObjectId: str}
