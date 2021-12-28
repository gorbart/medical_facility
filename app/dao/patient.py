from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.common import add_entity, delete_entity, get_entities, get_entity, update_entity

from datetime import datetime
from typing import Dict, List, Optional, Tuple
from app.models.patient import MedicinesTaken, Patient


async def get_patients(session: AsyncSession):
    return await get_entities(session, Patient)


async def get_patient(session: AsyncSession, patient_id: str):
    return await get_entity(session, Patient, patient_id)


# async def get_patient_by_name_and_surname(name: str, surname: str):
#     return await patient_collection.find_one({"name": name, "surname": surname})


async def add_patient(session: AsyncSession,patient_data: dict):
    return await add_entity(session, Patient, patient_data)


async def update_patient(session: AsyncSession, patient_id: str, patient_data: dict):
    return await update_entity(session, Patient, patient_data, patient_id)

# async def add_medicine(patient_id: str, medicine_data: MedicinesTaken):
#     patient = await get_patient(patient_id)
#     patient.medicine_taken.append(medicine_data)
#     return update_patient(patient_id, patient.dict())


# async def add_disease(patient_id: str, disease_data: dict):
#     patient = await get_patient(patient_id)
#     patient.disease_history.append(disease_data)
#     return update_patient(patient_id, patient.dict())


async def delete_patient(session: AsyncSession, patient_id: str):
    return await delete_entity(session, patient_id)
