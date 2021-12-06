from bson import json_util
from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import JSONResponse, Response

from app.dao.doctor import *
from app.models.doctor import Doctor, TimePeriod, Appointment, UpdateDoctor

DOCTOR_NOT_FOUND_MESSAGE = 'Doctor with id {} not found'
DOCTOR_NOT_CHANGED_MESSAGE = "Doctor data couldn't be changed"
DOCTOR_WITH_THIS_SPECIALTY_NOT_FOUND_MESSAGE = 'Doctor with specialty: {} not found'

router = APIRouter(
    prefix="/doctors",
    tags=["doctors"]
)


@router.get('/by_specialty/', response_description='Get a doctor with given specialty')
async def get_doctors_with_specialty(doctor_specialty: str) -> JSONResponse:
    doctors = await get_doctors_by_specialty(doctor_specialty)
    doctors = json_util.dumps(doctors)
    return JSONResponse(status_code=status.HTTP_200_OK, content=doctors)


@router.get('/one/', response_description='Get a doctor with given id')
async def get_one_doctor(doctor_id: str) -> JSONResponse:
    doctor = await get_doctor(doctor_id)
    doctor_json = json_util.dumps(doctor)
    if doctor is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=doctor_json)
    raise HTTPException(status_code=404, detail=DOCTOR_NOT_FOUND_MESSAGE.format(doctor_id))


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


@router.put('/', response_description='Update a doctor in database')
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

    if not doctor:
        raise HTTPException(status_code=404, detail=DOCTOR_NOT_FOUND_MESSAGE.format(doctor_id))

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

    if not doctor:
        raise HTTPException(status_code=404, detail=DOCTOR_NOT_FOUND_MESSAGE.format(doctor_id))

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


@router.delete('/', response_description='Delete a doctor from database')
async def delete_doctor_data(doctor_id: str) -> Response:
    if await delete_doctor(doctor_id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=DOCTOR_NOT_FOUND_MESSAGE.format(doctor_id))
