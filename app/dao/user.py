from app.dao.database import user_collection
from app.dao.common import add_entity, delete_entity, get_entities, get_entity, update_entity

async def get_users():
    return await get_entities(user_collection)


async def get_user(user_id: str):
    return await get_entity(user_collection, user_id)

async def get_user_by_login(login: str):
    return await user_collection.find_one({"login": login})


async def add_user(user_data: dict):
    return await add_entity(user_collection, user_data)


async def update_user(user_id: str, user_data: dict):
    return await update_entity(user_collection, user_data, user_id)


async def delete_user(user_id: str):
    return await delete_entity(user_collection, user_id)