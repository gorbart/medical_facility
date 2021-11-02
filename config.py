import motor.motor_asyncio
from decouple import config

# Get configuration of MongoDB Atlas from .env file
MONGO_DETAILS = config('MONGO_DETAILS')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

medical_facility_db = client.medical_facility

doctor_collection = medical_facility_db['doctors']
patient_collection = medical_facility_db['patient']
user_collection = medical_facility_db['user']