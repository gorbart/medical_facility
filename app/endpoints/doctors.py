from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from bson import json_util

from app.models.doctor import Doctor
from app.dao.doctor import *

DOCTOR_NOT_FOUND_MESSAGE = 'Doctor with id {} not found'

router = APIRouter(
    prefix="/doctors",
    tags=["doctors"]
)

@router.get('/{doctor_id}', response_description='Get a doctor with given id')
async def get_one_doctor(doctor_id: str) -> JSONResponse:
    doctor = await get_doctor(doctor_id)
    doctor = json_util.dumps(doctor)
    if doctor is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=doctor)
    raise HTTPException(status_code=404, detail=DOCTOR_NOT_FOUND_MESSAGE.format(doctor_id))


@router.get('/', response_description='Get all doctors')
async def get_doctor_list() -> JSONResponse:
    doctors = await get_doctors()
    doctors = json_util.dumps(doctors)
    return JSONResponse(status_code=status.HTTP_200_OK, content=doctors)

@router.post('/', response_description='Add a doctor')
async def add_doctor_data(doctor:Doctor) -> JSONResponse:
    db_doctor = await add_doctor(doctor.dict(by_alias=True))
    db_doctor = json_util.dumps(db_doctor)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=db_doctor)
