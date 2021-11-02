from app.models.base import Person

class User(Person):
    login: str
    password: str
