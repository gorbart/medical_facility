from datetime import datetime
from typing import Dict, List, Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dao.common import add_entity, delete_entity, get_entities, get_entity, update_entity
from app.models.doctor import Appointment, AppointmentInCreate, Doctor, DoctorSpecialtyLink, Specialty, SpecialtyEnum, \
    TimePeriod, TimePeriodInCreate, TimePeriodInResponse, WorkingHours, WorkingHoursInCreate


async def get_doctors(session: AsyncSession):
    stmt = select(Doctor)
    
    result = session.execute(stmt).scalars().all()
    
    return result


async def get_doctors_by_specialty(session: AsyncSession, specialty_name: str):
    stmt = select(Specialty).filter(Specialty.name == specialty_name)

    entity = session.execute(stmt).scalar()

    if entity:
        return entity.doctors

async def get_doctor(session: AsyncSession, doctor_id: str):
    return await get_entity(session, Doctor, doctor_id)


async def add_doctor(session: AsyncSession, doctor_data: dict):
    return await add_entity(session, doctor_data)


async def update_doctor(session: AsyncSession, doctor_id: str, doctor_data: dict):
    return await update_entity(session, Doctor, doctor_data, doctor_id)


async def add_time_period(session: AsyncSession, time_period_data: dict):
    return await add_entity(session, time_period_data)


async def add_working_hours(session: AsyncSession, working_hours_data: dict):
    return await add_entity(session, working_hours_data)


async def get_doctors_time_period(session: AsyncSession, doctor_id):
    stmt = select(TimePeriod).where(TimePeriod.doctor_id == doctor_id)

    time_periods = session.execute(stmt).scalars().all()

    result = []

    for period in time_periods:
        stmt = select(WorkingHours).where(WorkingHours.time_period_id == period.id)
        working_hours = session.execute(stmt).scalars().all()

        hours = [WorkingHoursInCreate(date=work.date, until=work.until) for work in working_hours]

        result.append(TimePeriodInResponse(date=period.date, until=period.until, working_hours=hours))

    return result


# async def update_doctor_schedule(session: AsyncSession,
#         doctor_id: str, new_schedule: Dict[Tuple[datetime, datetime],
#                                            List[Tuple[datetime, datetime]]]):

#     doctor = await get_doctor(session, doctor_id)

#     for period in new_schedule.keys():

#         schedule = await add_entity(session, TimePeriod(**{"date": period[0], "doctor_id":doctor_id}))

#         session.refresh(schedule)

#         for hours in new_schedule[period]:
#             await add_entity(session, WorkingHours(time_period_id=schedule.id, date=hours[0], until=hours[1]))


#     return doctor


async def add_appointment(session: AsyncSession,
                          appointment: dict):
    return await add_entity(session, appointment)


async def get_doctors_appointments(session: AsyncSession, doctor_id: str):
    stmt = select(Appointment).where(Appointment.doctor_id == doctor_id)

    appointments = session.execute(stmt).scalars().all()

    return appointments

async def get_appointment(session: AsyncSession, appointment_id: str):
    return await get_entity(session, Appointment, appointment_id)

async def update_appointment(session: AsyncSession,
                             appointment_id: str, appointment: AppointmentInCreate):
    appointment = await update_entity(session, Appointment, appointment, appointment_id)

    session.refresh(appointment)

    return appointment

async def delete_appointment(session: AsyncSession, appointment_id: str):
    return await delete_entity(session, Appointment, appointment_id)


async def update_doctor_specialty(session: AsyncSession, doctor_id: str, new_specialty: str):
    doctor = await get_doctor(session, doctor_id)

    stmt = select(Specialty).filter(Specialty.name == new_specialty)

    specialty = session.execute(stmt).scalar()

    if not specialty:
        specialty = await add_entity(session, Specialty(**{"name": SpecialtyEnum(new_specialty)}))
        session.refresh(specialty)

    specialty.doctors.append(doctor)

    session.add(specialty)

    session.commit()

    session.refresh(doctor)

    return doctor


async def delete_doctor(session: AsyncSession, doctor_id: str):
    return await delete_entity(session, Doctor, doctor_id)
