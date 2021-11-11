import pytest

from app.models.user import UserType
from app.dao import user as dao_user



@pytest.mark.asyncio
async def test_create_user():

    data = {
        'name': 'name',
        'surname': 'surname',
        'login': 'login',
        'password': 'password',
        'user_type': UserType.NURSE
    }

    user = await dao_user.add_user(data)

    assert user.name == 'name'
