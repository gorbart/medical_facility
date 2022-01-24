from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.dao.common import add_entity, delete_entity, get_entities, get_entity, update_entity

from datetime import datetime
from typing import Dict, List, Optional, Tuple
from app.models.patient import Disease, Medicine, MedicinesTaken, MedicinesTakenInCreate, Patient, UpdatePatient


async def get_patients(session: AsyncSession):
    return await get_entities(session, Patient)


async def get_patient(session: AsyncSession, patient_id: str):
    patient = await get_entity(session, Patient, patient_id)
    
    return patient

async def get_medicines(session: AsyncSession, patient_id: str):
    
    stmt = select(MedicinesTaken, Medicine).join(Medicine, MedicinesTaken.id == Medicine.medicines_taken_id).filter(MedicinesTaken.patient_id == patient_id)
    
    taken = session.execute(stmt)
    
    
    
    return taken

async def get_diseases(session: AsyncSession, patient_id: str):
    
    stmt = select(Disease).where(Disease.patient_id == patient_id)
    
    diseases = session.execute(stmt)
    
    return diseases


async def get_patient_by_name_and_surname(session: AsyncSession,name: str, surname: str):
    stmt = select(Patient).filter(Patient.name == name).filter(Patient.surname == surname)
    
    entity = session.execute(stmt)
    
    if entity:
        return entity.scalar()


async def add_patient(session: AsyncSession,patient_data: dict):
    return await add_entity(session, patient_data)


async def update_patient(session: AsyncSession, patient_id: str, patient_data: UpdatePatient):
    return await update_entity(session, Patient, patient_data.dict(), patient_id)

async def add_medicine_to_patient(session: AsyncSession,patient_id: str, medicine_data: MedicinesTakenInCreate):
    
    patient = await get_patient(session, patient_id)
    
    medicines_taken = await add_entity(session, MedicinesTaken(**{"date": medicine_data.date, "patient_id": patient.id}))
    
    for medicine in medicine_data.medicines:
        medicine["medicines_taken_id"] = medicines_taken.id
        await add_entity(session, Medicine(**medicine))
        
    session.refresh(patient)
    
    return patient


async def add_disease_to_patient(session: AsyncSession, patient_id: str, disease_data: dict):
    
    patient = await get_patient(session, patient_id)
    
    disease_taken = await add_entity(session, Disease(patient_id=patient.id, **disease_data))
    
    session.refresh(patient)
    
    return patient

async def delete_patient(session: AsyncSession, patient_id: str):
    return await delete_entity(session, patient_id)
