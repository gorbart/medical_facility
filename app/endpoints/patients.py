from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import JSONResponse, Response
from bson import json_util

from app.models.patient import Patient, MedicinesTaken
from app.dao.patient import *


PATIENT_NOT_FOUND_MESSAGE = 'Patient with id {} not found'
OBJECT_NOT_CHANGED_MESSAGE = "Patient data couldn't be changed"

router = APIRouter(
    prefix="/patients",
    tags=["patients"]
)


@router.get('/{patient_id}', response_description='Get a patient with given id')
async def get_one_patient(patient_id: str) -> JSONResponse:
    patient = await get_patient(patient_id)
    patient = json_util.dumps(patient)
    if patient is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=patient)
    raise HTTPException(status_code=404, detail=PATIENT_NOT_FOUND_MESSAGE.format(patient_id))


@router.get('/', response_description='Get all patients')
async def get_patient_list() -> JSONResponse:
    patients = await get_patients()
    patients = json_util.dumps(patients)
    return JSONResponse(status_code=status.HTTP_200_OK, content=patients)


@router.post('/', response_description='Add a patient')
async def add_patient_data(patient: Patient) -> JSONResponse:
    db_patient = await add_patient(patient.dict(by_alias=True))
    db_patient = json_util.dumps(db_patient)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=db_patient)


@router.put('/{patient_id}', response_description='Update a patient in database')
async def update_patient_data(patient_id: str, received_patient_data: dict) -> JSONResponse:
    is_successful = await update_patient(patient_id, received_patient_data)

    patient = await get_patient(patient_id)

    if patient is not None:
        patient = json_util.dumps(patient)
        if not is_successful:
            return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={'message': OBJECT_NOT_CHANGED_MESSAGE,
                                                                               'object': patient})
        else:
            return JSONResponse(status_code=status.HTTP_200_OK, content=patient)

    raise HTTPException(status_code=404, detail=PATIENT_NOT_FOUND_MESSAGE.format(patient_id))

@router.put('/add_medicine/', response_description='Add a medicine')
async def add_medicine(patient_id :str, medicine_data: MedicinesTaken) ->JSONResponse:
    patient = await get_patient(patient_id)
    patient['medicine_taken'].append(medicine_data) 
    is_successful = await update_patient(patient_id, patient)
    if patient is not None:
        patient = json_util.dumps(patient)
        if not is_successful:
            return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={'message': OBJECT_NOT_CHANGED_MESSAGE,
                                                                               'object': patient})
        else:
            return JSONResponse(status_code=status.HTTP_200_OK, content=patient)
    raise HTTPException(status_code=404, detail=PATIENT_NOT_FOUND_MESSAGE.format(patient_id))

@router.put('/add_disease/', response_description='Add a disease')
async def add_disease(patient_id :str, disease_data: dict) ->JSONResponse:
    patient = await get_patient(patient_id)
    patient['disease_history'].append(disease_data)
    
    is_successful = await update_patient(patient_id, patient)
    if patient is not None:
        patient = json_util.dumps(patient)
        if not is_successful:
            return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={'message': OBJECT_NOT_CHANGED_MESSAGE,
                                                                               'object': patient})
        else:
            return JSONResponse(status_code=status.HTTP_200_OK, content=patient)
    raise HTTPException(status_code=404, detail=PATIENT_NOT_FOUND_MESSAGE.format(patient_id))


@router.delete('/{patient_id}', response_description='Delete a patient from database')
async def delete_patient_data(patient_id: str) -> Response:
    if await delete_patient(patient_id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=PATIENT_NOT_FOUND_MESSAGE.format(patient_id))


