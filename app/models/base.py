from typing import Optional
from bson import ObjectId
# from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field


# class PyObjectId(ObjectId):
#     """
#     Class PyObjectId maps MongoDB BSON id to JSON format, which is used by FastAPI.
#     """

#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate

#     @classmethod
#     def validate(cls, v):
#         if not ObjectId.is_valid(v):
#             raise ValueError('Invalid objectid')
#         return ObjectId(v)

#     @classmethod
#     def __modify_schema__(cls, field_schema):
#         field_schema.update(type='string')


class DBModel(SQLModel):
    """
    DBModel class has id attribute which is a common attribute for all models being saved into database. It's
    automatically assigned to a model on its creation
    """

    id: int = Field(default=None, primary_key=True)
    

class Person(DBModel):
    name: str
    surname: str
    email: Optional[str]
    phone_number: Optional[str]


class UpdatePerson(SQLModel):
    name: Optional[str]
    surname: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]
