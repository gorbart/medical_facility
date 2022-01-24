from bson import json_util
from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.params import Depends
from starlette import status
from starlette.responses import JSONResponse, Response
from app.dao.database import get_session

from app.dao.doctor import *
from app.models.doctor import Doctor, DoctorResponse, TimePeriod, Appointment, TimePeriodInCreate, UpdateDoctor

DOCTOR_NOT_FOUND_MESSAGE = 'Doctor with id {} not found'
DOCTOR_NOT_CHANGED_MESSAGE = "Doctor data couldn't be changed"
DOCTOR_WITH_THIS_SPECIALTY_NOT_FOUND_MESSAGE = 'Doctor with specialty: {} not found'

router = APIRouter(
    prefix="/doctors",
    tags=["doctors"]
)


@router.get('/by_specialty/', response_description='Get doctors with given specialty')
async def get_doctors_with_specialty(doctor_specialty: str, session=Depends(get_session)) -> JSONResponse:
    doctors = await get_doctors_by_specialty(session, doctor_specialty)
    if not doctors:
        raise HTTPException(status_code=404, detail=DOCTOR_WITH_THIS_SPECIALTY_NOT_FOUND_MESSAGE.format(doctor_specialty))
    return JSONResponse(status_code=status.HTTP_200_OK, content=[doctor.as_dict() for doctor in doctors])


@router.get('/one/', response_description='Get a doctor with given id')
async def get_one_doctor(doctor_id: str, session=Depends(get_session)) -> JSONResponse:
    doctor = await get_doctor(session, doctor_id)
    if doctor is not None:
        schedule = await get_doctors_time_period(session, doctor_id)
    
        appointments = await get_doctors_appointments(session, doctor_id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(DoctorResponse(**doctor.as_dict(), schedule=schedule, scheduled_appointments=appointments, specialties=doctor.specialties)))
    raise HTTPException(status_code=404, detail=DOCTOR_NOT_FOUND_MESSAGE.format(doctor_id))


@router.get('/', response_description='Get all doctors')
async def get_doctor_list(session=Depends(get_session)) -> JSONResponse:
    doctors = await get_doctors(session)
    return JSONResponse(status_code=status.HTTP_200_OK, content=[doctor.as_dict() for doctor in doctors])


@router.post('/', response_description='Add a doctor')
async def add_doctor_data(doctor: Doctor, specialties: List[str], session=Depends(get_session)) -> JSONResponse:
    db_doctor = await add_doctor(session, doctor)
    for specialty in specialties:
        db_doctor = await update_doctor_specialty(session, db_doctor.id, specialty)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=db_doctor.as_dict())


@router.put('/specialty', response_description="Add doctor's specialty")
async def add_doctor_specialty(doctor_id: str, specialty: str, session=Depends(get_session)) -> JSONResponse:
    db_doctor = await update_doctor_specialty(session, doctor_id, specialty)

    schedule = await get_doctors_time_period(session, doctor_id)
    
    appointments = await get_doctors_appointments(session, doctor_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(DoctorResponse(**db_doctor.as_dict(), schedule=schedule, scheduled_appointments=appointments, specialties=db_doctor.specialties)))
  


@router.put('/', response_description='Update a doctor in database')
async def update_doctor_data(doctor_id: str, received_doctor_data: UpdateDoctor, session=Depends(get_session)) -> JSONResponse:
    doctor = await get_doctor(session, doctor_id)
    
    if not doctor:
        raise HTTPException(status_code=404, detail=DOCTOR_NOT_FOUND_MESSAGE.format(doctor_id))
    
    is_successful = await update_doctor(session, doctor_id, received_doctor_data.dict(by_alias=True))

    schedule = await get_doctors_time_period(session, doctor_id)
    
    appointments = await get_doctors_appointments(session, doctor_id)
            
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(DoctorResponse(**doctor.as_dict(), schedule=schedule, scheduled_appointments=appointments, specialties=doctor.specialties)))



@router.put('/add_time_period/', response_description='Add a time period')
async def add_time_period_data(doctor_id: str, time_period: TimePeriodInCreate, session=Depends(get_session)) -> JSONResponse:
    doctor = await get_doctor(session, doctor_id)

    if not doctor:
        raise HTTPException(status_code=404, detail=DOCTOR_NOT_FOUND_MESSAGE.format(doctor.id))

    db_time_period = await add_time_period(session, TimePeriod(date=time_period.date, until=time_period.until, doctor_id=doctor.id))
    
    for work in time_period.working_hours:
        await add_working_hours(session, WorkingHours(**work.dict(), time_period_id=db_time_period.id))

    schedule = await get_doctors_time_period(session, doctor_id)
    
    appointments = await get_doctors_appointments(session, doctor_id)
            
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(DoctorResponse(**doctor.as_dict(), schedule=schedule, scheduled_appointments=appointments, specialties=doctor.specialties)))


@router.put('/add_appointment/', response_description='Add an appointment')
async def add_appointment_data(doctor_id: str, appointment: AppointmentInCreate, session=Depends(get_session)) -> JSONResponse:
    doctor = await get_doctor(session, doctor_id)

    if not doctor:
        raise HTTPException(status_code=404, detail=DOCTOR_NOT_FOUND_MESSAGE.format(doctor_id))

    db_appointment = await add_appointment(session, Appointment(**appointment.dict(), doctor_id=doctor.id))

    schedule = await get_doctors_time_period(session, doctor_id)
    
    appointments = await get_doctors_appointments(session, doctor_id)

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(DoctorResponse(**doctor.as_dict(), schedule=schedule, scheduled_appointments=appointments, specialties=doctor.specialties)))


@router.delete('/', response_description='Delete a doctor from database')
async def delete_doctor_data(doctor_id: str, session=Depends(get_session)) -> Response:
    if await delete_doctor(doctor_id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=DOCTOR_NOT_FOUND_MESSAGE.format(doctor_id))
