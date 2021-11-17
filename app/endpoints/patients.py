from fastapi import APIRouter, HTTPException
from fastapi.params import Body
from starlette import status
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import json_util

from app.models.patient import Patient
from app.dao.patient import *


PATIENT_NOT_FOUND_MESSAGE = 'Patient with id {} not found'

router = APIRouter(
    prefix="/patients",
    tags=["patients"]
)

async def convert_to_standard_model(entity: dict, entity_class):
    entity = entity_class(**entity).dict()
    entity['_id'] = entity.pop('id')
    return entity

@router.get('/{patient_id}', response_description='Get a patient with given id')
async def get_one_patient(patient_id: str) -> JSONResponse:
    patient = await get_patient(patient_id)
    print(patient)
    if patient is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=patient)
    raise HTTPException(status_code=404, detail=PATIENT_NOT_FOUND_MESSAGE.format(patient_id))


@router.get('/', response_description='Get all patients')
async def get_patient_list() -> JSONResponse:
    patients = await get_patients()
    return JSONResponse(status_code=status.HTTP_200_OK, content=patients)


@router.post('/', response_description='Add a patient')
async def add_patient_data(raw_patient:Patient = Body(...)) -> JSONResponse:
    raw_patient = jsonable_encoder(raw_patient)
    patient = await convert_to_standard_model(raw_patient, Patient)
    # dict with attributes gets converted into a model class object
    new_patient = await add_patient(patient)
    new_patient = json_util.dumps(new_patient)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_patient)
