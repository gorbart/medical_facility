from sqlite3.dbapi2 import IntegrityError
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
import sqlalchemy
from starlette import status
from starlette.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from bson import json_util
from app.dao.database import get_session

from app.models.user import User
from app.dao.user import *

USER_NOT_FOUND_MESSAGE = 'User with id {} not found'
INCORRECT_LOGIN_DATA = 'Sorry, we can not find the acccount with entered login, or the password is incorrect'
USER_NOT_CHANGED_MESSAGE = 'Unfortunatelly, user with id {} data did not change'

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get('/one', response_description='Get a user with given id')
async def get_one_user(user_id: str, session=Depends(get_session)) -> JSONResponse:
    user = await get_user(session, user_id)
    if user is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=user.as_dict())
    raise HTTPException(status_code=404, detail=USER_NOT_FOUND_MESSAGE.format(user_id))


@router.get('/', response_description='Get all users')
async def get_user_list(session=Depends(get_session)) -> JSONResponse:
    users = await get_users(session)
    return JSONResponse(status_code=status.HTTP_200_OK, content=[user.as_dict() for user in users])


@router.get('/login/', response_description='log in')
async def log_in(login: str, password: str, session=Depends(get_session)) -> JSONResponse:
    user = await get_user_by_login(session, login)
    if user:
        if user.password == password:
            return JSONResponse(status_code=status.HTTP_200_OK, content=user.as_dict())
    raise HTTPException(status_code=401, detail=INCORRECT_LOGIN_DATA)


@router.post('/', response_description='Add a user')
async def add_user_data(user: User, session=Depends(get_session)) -> JSONResponse:
    db_user = await add_user(session, user)
    if not db_user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="User with given login already exists")
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=db_user.as_dict())


@router.put('/', response_description='Update a user in database')
async def update_user_data(user_id: str, received_user_data: dict, session=Depends(get_session)) -> JSONResponse:
    user = await update_user(session, user_id,received_user_data)

    if user is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=user.as_dict())

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=USER_NOT_FOUND_MESSAGE.format(user_id))


@router.delete('/', response_description='Delete a user from database')
async def delete_user_data(user_id: str, session=Depends(get_session)) -> Response:
    if await delete_user(session, user_id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=USER_NOT_FOUND_MESSAGE.format(user_id))
