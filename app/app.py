from fastapi import FastAPI
from app.endpoints import doctors, users, patients

app = FastAPI()

app.include_router(doctors.router)
app.include_router(patients.router)
app.include_router(users.router)