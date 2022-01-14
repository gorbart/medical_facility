import enum
from bson.objectid import ObjectId
from sqlalchemy.sql.schema import UniqueConstraint
from sqlalchemy.sql.sqltypes import VARCHAR
from sqlmodel import Field, Column, Enum

from app.models.base import DBModel, Person


class UserType(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    NURSE = "nurse"


class User(Person, DBModel, table=True):
    login: str = Field(sa_column=Column("login", VARCHAR, primary_key=True))
    password: str
    user_type: UserType = Field(sa_column=Column(Enum(UserType), primary_key=True))
    id: int = None
    
    # class Config:
    #     arbitrary_types_allowed = True
    #     json_encoders = {ObjectId: str}
