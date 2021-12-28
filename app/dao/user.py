from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.common import add_entity, delete_entity, get_entities, get_entity, update_entity
from app.models.user import User


async def get_users(session: AsyncSession):
    return await get_entities(session, User)


async def get_user(session: AsyncSession, user_id: str):
    return await get_entity(session, User, user_id)


# async def get_user_by_login(login: str):
#     return await user_collection.find_one({"login": login})


async def add_user(session: AsyncSession, user_data: dict):
    return await add_entity(session, User, user_data)


async def update_user(session: AsyncSession, user_id: str, user_data: dict):
    return await update_entity(session, User, user_data, user_id)


async def delete_user(session: AsyncSession, user_id: str):
    return await delete_entity(session, User, user_id)
