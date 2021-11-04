from config import patient_collection
from app.dao.common import add_entity, delete_entity, get_entities, get_entity, update_entity

async def get_patients():
    return await get_entities(patient_collection)


async def get_patient(patient_id: str):
    return await get_entity(patient_collection, patient_id)

async def get_patient_by_name_and_surname(name: str, surname: str):
    return await patient_collection.find_one({"name": name, "surname": surname})


async def add_patient(patient_data: dict):
    return await add_entity(patient_collection, patient_data)


async def update_patient(patient_id: str, patient_data: dict):
    return await update_entity(patient_collection, patient_data, patient_id)

async def add_medicine(patient_id: str, medicine_data: dict):
    patient = await get_patient(patient_id)
    patient.medicine_taken.append(medicine_data)
    return update_patient(patient_id, patient.dict())

async def add_disease(patient_id: str, disease_data: dict):
    patient = await get_patient(patient_id)
    patient.disease_history.append(disease_data)
    return update_patient(patient_id, patient.dict())


async def delete_patient(patient_id: str):
    return await delete_entity(patient_collection, patient_id)