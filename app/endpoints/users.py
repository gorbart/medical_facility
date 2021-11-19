from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from bson import json_util

from app.models.user import User
from app.dao.user import *

USER_NOT_FOUND_MESSAGE = 'User with id {} not found'
INCORRECT_LOGIN_DATA = 'Sorry, we can not find the acccount with entered login, or the password is incorrect'
USER_NOT_CHANGED_MESSAGE = 'Unfortunatelly, user with id {} data did not change'

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get('/{user_id}', response_description='Get a user with given id')
async def get_one_user(user_id: str) -> JSONResponse:
    user = await get_user(user_id)
    user = json_util.dumps(user)
    if user is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=user)
    raise HTTPException(status_code=404, detail=USER_NOT_FOUND_MESSAGE.format(user_id))


@router.get('/', response_description='Get all users')
async def get_user_list() -> JSONResponse:
    users = await get_users()
    users = json_util.dumps(users)
    return JSONResponse(status_code=status.HTTP_200_OK, content=users)


@router.get('/login/', response_description='log in')
async def log_in(login: str, password: str) -> JSONResponse:
    user = await get_user_by_login(login)
    if user:
        if user['password'] == password:
            user_id = json_util.dumps(user['_id'])
            return JSONResponse(status_code=status.HTTP_200_OK, content=user_id)
    raise HTTPException(status_code=401, detail=INCORRECT_LOGIN_DATA)


@router.post('/', response_description='Add a user')
async def add_user_data(user: User) -> JSONResponse:
    db_user = await add_user(user.dict(by_alias=True))
    db_user = json_util.dumps(db_user)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=db_user)


@router.put('/{user_id}', response_description='Update a user in database')
async def update_user_data(user_id: str, received_user_data: dict) -> JSONResponse:
    is_successful = await update_user(user_id, received_user_data)

    user = await get_user(user_id)

    if user is not None:
        user = json_util.dumps(user)
        if not is_successful:
            return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                                content={'message': USER_NOT_CHANGED_MESSAGE.format(user_id),
                                         'object': user})
        else:
            return JSONResponse(status_code=status.HTTP_200_OK, content=user)

    raise HTTPException(status_code=404, detail=USER_NOT_FOUND_MESSAGE.format(user_id))


@router.delete('/{user_id}', response_description='Delete a user from database')
async def delete_user_data(user_id: str) -> Response:
    if await delete_user(user_id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=USER_NOT_FOUND_MESSAGE.format(user_id))
