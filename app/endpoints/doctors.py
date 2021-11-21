from bson import json_util
from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import JSONResponse, Response

from app.dao.doctor import *
from app.models.doctor import Doctor, TimePeriod, Appointment, UpdateDoctor

DOCTOR_NOT_FOUND_MESSAGE = 'Doctor with id {} not found'
DOCTOR_NOT_CHANGED_MESSAGE = "Doctor data couldn't be changed"
DOCTOR_WITH_THIS_SPECIALITY_NOT_FOUND_MESSAGE = 'Doctor with speciality: {} not found'

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


@router.get('/by_speciality/', response_description='Get a doctor with given speciality')
async def get_doctors_with_speciality(doctor_speciality: str) -> JSONResponse:
    doctors = await get_doctors_by_speciality(doctor_speciality)
    doctors = json_util.dumps(doctors)
    return JSONResponse(status_code=status.HTTP_200_OK, content=doctors)


@router.get('/', response_description='Get all doctors')
async def get_doctor_list() -> JSONResponse:
    doctors = await get_doctors()
    doctors = json_util.dumps(doctors)
    return JSONResponse(status_code=status.HTTP_200_OK, content=doctors)


@router.post('/', response_description='Add a doctor')
async def add_doctor_data(doctor: Doctor) -> JSONResponse:
    db_doctor = await add_doctor(doctor.dict(by_alias=True))
    db_doctor = json_util.dumps(db_doctor)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=db_doctor)


@router.put('/{doctor_id}', response_description='Update a doctor in database')
async def update_doctor_data(doctor_id: str, received_doctor_data: UpdateDoctor) -> JSONResponse:
    is_successful = await update_doctor(doctor_id, received_doctor_data.dict(by_alias=True))

    doctor = await get_doctor(doctor_id)

    if doctor is not None:
        doctor = json_util.dumps(doctor)
        if not is_successful:
            return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={'message': DOCTOR_NOT_CHANGED_MESSAGE,
                                                                               'object': doctor})
        else:
            return JSONResponse(status_code=status.HTTP_200_OK, content=doctor)

    raise HTTPException(status_code=404, detail=DOCTOR_NOT_FOUND_MESSAGE.format(doctor_id))


@router.put('/add_time_period/', response_description='Add a time period')
async def add__time_period(doctor_id: str, time_period: TimePeriod) -> JSONResponse:
    doctor = await get_doctor(doctor_id)
    doctor['schedule'].append(time_period)

    is_successful = await update_doctor(doctor_id, doctor)

    if doctor is not None:
        doctor = json_util.dumps(doctor)
        if not is_successful:
            return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={'message': DOCTOR_NOT_CHANGED_MESSAGE,
                                                                               'object': doctor})
        else:
            return JSONResponse(status_code=status.HTTP_200_OK, content=doctor)

    raise HTTPException(status_code=404, detail=DOCTOR_NOT_FOUND_MESSAGE.format(doctor_id))


@router.put('/add_appointment/', response_description='Add an appointment')
async def add_appointment(doctor_id: str, appointment: Appointment) -> JSONResponse:
    doctor = await get_doctor(doctor_id)
    doctor['scheduled_appointments'].append(appointment)

    is_successful = await update_doctor(doctor_id, doctor)

    if doctor is not None:
        doctor = json_util.dumps(doctor)
        if not is_successful:
            return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={'message': DOCTOR_NOT_CHANGED_MESSAGE,
                                                                               'object': doctor})
        else:
            return JSONResponse(status_code=status.HTTP_200_OK, content=doctor)

    raise HTTPException(status_code=404, detail=DOCTOR_NOT_FOUND_MESSAGE.format(doctor_id))


@router.delete('/{doctor_id}', response_description='Delete a doctor from database')
async def delete_doctor_data(doctor_id: str) -> Response:
    if await delete_doctor(doctor_id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=DOCTOR_NOT_FOUND_MESSAGE.format(doctor_id))
