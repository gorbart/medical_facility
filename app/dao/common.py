from typing import Type
from bson import ObjectId
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exc

from app.models.base import DBModel

# from motor.motor_asyncio import AsyncIOMotorCollection


async def get_entities(session: AsyncSession, model_cls: Type[DBModel]):
    stmt = select(model_cls)
    
    result = session.execute(stmt).scalars().all()
    
    return [model_cls(**(dict(entity))) for entity in result]
    
    


async def get_entity(session: AsyncSession, model_cls: Type[DBModel], entity_id: str):
    stmt = select(model_cls).filter(model_cls.id == entity_id)
    
    entity = session.execute(stmt)
    
    if entity:
        return entity.scalar()


async def add_entity(session: AsyncSession,entity_data: DBModel):
    
    session.add(entity_data)
    
    try:
        session.commit()
    except exc.IntegrityError as e:
        print(e)
        session.rollback()
        return None

    
    session.refresh(entity_data)

    return entity_data


async def update_entity(session: AsyncSession, model_cls: Type[DBModel], entity_data: dict, entity_id: str):
    """Function returns False if request body is empty or entity with given id doesn't exist"""
   
    stmt = select(model_cls).filter(model_cls.id == entity_id)
    
    result = session.execute(stmt)
    
    entity = result.scalar()
    
    if entity:
        for key in entity_data.keys():
            setattr(entity, key,entity_data[key])
                            
        session.add(entity)
        session.commit()
        return entity

    return None


async def delete_entity(session: AsyncSession, model_cls: Type[DBModel],entity_id: str):
    """Function returns False if entity with given id doesn't exist"""
    entity = await session.query(model_cls).filter(model_cls.id == entity_id).first()
    if entity:
        await session.delete(entity)
        session.commit()
        return True
    return False
