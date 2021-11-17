from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.models.patient import Patient
from app.dao.patient import *


PATIENT_NOT_FOUND_MESSAGE = 'Patient with id {} not found'

router = APIRouter(
    prefix="/patients",
    tags=["patients"]
)

@router.get('/{patient_id}', response_description='Get a patient with given id')
async def get_one_patient(patient_id: str) -> JSONResponse:
    patient = await get_patient(patient_id)
    if patient is not None:
        return JSONResponse(status_code.HTTP_200_OK, content=patient)
    raise HTTPException(status_code=404, detail=PATIENT_NOT_FOUND_MESSAGE.format(patient_id))

@router.get('/', response_description='Get all patients')
async def get_patient_list() -> JSONResponse:
    patients = await get_patients()
    return JSONResponse(status_code=status.HTTP_200_OK, content=patients)

@router.post('/', response_description='Add a patient')
async def add_patient_data(patient:Patient) -> JSONResponse:
    
    name = patient.name
    surname = patient.surname
    email = patient.email
    phone = patient.phone_number
    disease_history = patient.disease_history
    medicine_taken = patient.medicine_taken
    patient_dict = {
        "name":name,
        "surname":surname,
        "email":email,
        "phone":phone,
        "disease_history":disease_history,
        "medicine_taken":medicine_taken
    }

    await add_patient(patient_dict)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=patient_dict)