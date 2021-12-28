from bson import json_util
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from starlette import status
from starlette.responses import JSONResponse, Response
from app.dao.database import get_session

from app.dao.patient import *
from app.models.patient import Patient, UpdatePatient

PATIENT_NOT_FOUND_MESSAGE = 'Patient with id {} not found'
OBJECT_NOT_CHANGED_MESSAGE = "Patient data couldn't be changed"

router = APIRouter(
    prefix="/patients",
    tags=["patients"]
)


@router.get('/one', response_description='Get a patient with given id')
async def get_one_patient(patient_id: str, session=Depends(get_session)) -> JSONResponse:
    patient = await get_patient(session, patient_id)
    if patient is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=patient.as_dict())
    raise HTTPException(status_code=404, detail=PATIENT_NOT_FOUND_MESSAGE.format(patient_id))


@router.get('/', response_description='Get all patients')
async def get_patient_list(session=Depends(get_session)) -> JSONResponse:
    patients = await get_patients(session)
    return JSONResponse(status_code=status.HTTP_200_OK, content=[patient.as_dict() for patient in patients])


@router.post('/', response_description='Add a patient')
async def add_patient_data(patient: Patient, session=Depends(get_session)) -> JSONResponse:
    db_patient = await add_patient(session, patient)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=db_patient.as_dict())


@router.put('/', response_description='Update a patient in database')
async def update_patient_data(patient_id: str, received_patient_data: UpdatePatient, session=Depends(get_session)) -> JSONResponse:
    patient = await update_patient(session, patient_id, received_patient_data)

    if patient is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=patient.as_dict())

    raise HTTPException(status_code=404, detail=PATIENT_NOT_FOUND_MESSAGE.format(patient_id))


@router.put('/add_medicine/', response_description='Add a medicine')
async def add_medicine(patient_id: str, medicine_data: MedicinesTakenInCreate, session=Depends(get_session)) -> JSONResponse:
    patient = await get_patient(session, patient_id)
    
    if not patient:
        raise HTTPException(status_code=404, detail=PATIENT_NOT_FOUND_MESSAGE.format(patient_id))
    
    updated_patient = await add_medicine_to_patient(session, patient_id, medicine_data)

    if updated_patient is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=patient.as_dict())

    raise HTTPException(status_code=404, detail=PATIENT_NOT_FOUND_MESSAGE.format(patient_id))


@router.put('/add_disease/', response_description='Add a disease')
async def add_disease(patient_id: str, disease_data: dict, session=Depends(get_session)) -> JSONResponse:
    patient = await get_patient(session, patient_id)
    
    if not patient:
        raise HTTPException(status_code=404, detail=PATIENT_NOT_FOUND_MESSAGE.format(patient_id))
    
    updated_patient = await add_disease_to_patient(session, patient_id, disease_data)

    if updated_patient is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=patient.as_dict())

    raise HTTPException(status_code=404, detail=PATIENT_NOT_FOUND_MESSAGE.format(patient_id))


@router.delete('/', response_description='Delete a patient from database')
async def delete_patient_data(patient_id: str, session=Depends(get_session)) -> Response:
    if await delete_patient(patient_id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=PATIENT_NOT_FOUND_MESSAGE.format(patient_id))
