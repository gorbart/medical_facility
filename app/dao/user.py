from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.dao.common import add_entity, delete_entity, get_entities, get_entity, update_entity
from app.models.user import User, UserType


async def get_users(session: AsyncSession):
    return await get_entities(session, User)


async def get_user_by_login_and_type(session: AsyncSession, login: str, user_type: UserType):
    stmt = select(User).filter(User.login == login and User.user_type == user_type)
    
    entity = session.execute(stmt)
    
    if entity:
        return entity.scalar()
    


async def add_user(session: AsyncSession, user_data: dict):
    return await add_entity(session, user_data)


async def update_user(session: AsyncSession, user_id: str, user_data: dict):
    return await update_entity(session, user_data, user_id)


async def delete_user(session: AsyncSession, user_id: str):
    return await delete_entity(session, user_id)
