from fastapi import FastAPI
from app.dao.database import init_db
from app.endpoints import doctors, users, patients
from fastapi.middleware.cors import CORSMiddleware

description = """
Medical facility API helps managing medical facility.

## Patients

You can create, read, update and delete data about **Patients**

## Doctors

You can create, read, update and delete data about **Doctors**

You are able to:

* Add doctors' schedule
* Add scheduled appointments
* Search doctors by specialty 

"""

tags_metadata = [
    {
        "name": "patients",
        "description": "Operations with patients."
    },
    {
        "name": "doctors",
        "description": "Operations with doctors."
    },
    {
        "name": "users",
        "description": "Operations with users. Login logic is here too."
    }
]

app = FastAPI(
    title="Medical facility",
    version="0.0.2",
    description=description,
    openapi_tags=tags_metadata
)


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(doctors.router)
app.include_router(patients.router)
app.include_router(users.router)
# Allow cors so api can be used from browser
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
