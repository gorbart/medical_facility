from typing import Type
from bson import ObjectId
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import DBModel

# from motor.motor_asyncio import AsyncIOMotorCollection


async def get_entities(session: AsyncSession, model_cls: Type[DBModel]):
    result = await session.execute(select(model_cls))
    return result


async def get_entity(session: AsyncSession, model_cls: Type[DBModel], entity_id: str):
    entity = await session.query(model_cls).filter(model_cls.id == entity_id).first()
    if entity:
        return entity


async def add_entity(session: AsyncSession, entity_data: DBModel):
    entity = await session.add(entity_data)
    await session.commit()
    await session.refresh(entity_data)

    return entity_data


async def update_entity(session: AsyncSession, model_cls: Type[DBModel], entity_data: dict, entity_id: str):
    """Function returns False if request body is empty or entity with given id doesn't exist"""
    if len(entity_data) < 1:
        return None
    entity = await session.query(model_cls).filter(model_cls.id == entity_id).first()
    if entity:
        updated_entity = model_cls(id=entity.id, **entity_data)
        session.commit()

    return None


async def delete_entity(session: AsyncSession, model_cls: Type[DBModel],entity_id: str):
    """Function returns False if entity with given id doesn't exist"""
    entity = await session.query(model_cls).filter(model_cls.id == entity_id).first()
    if entity:
        await session.delete(entity)
        session.commit()
        return True
    return False
