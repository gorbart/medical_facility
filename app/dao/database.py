# import motor.motor_asyncio
from decouple import config
# import certifi
from sqlmodel import create_engine, SQLModel, Session


# Get configuration of MongoDB Atlas from .env file
DATABASE_URL = config('DATABASE_URL')

# client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL, tlsCAFile=certifi.where())

# medical_facility_db = client.medical_facility

# doctor_collection = medical_facility_db['doctors']
# patient_collection = medical_facility_db['patient']
# user_collection = medical_facility_db['user']

engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
