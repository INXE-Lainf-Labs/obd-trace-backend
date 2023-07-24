from http import HTTPStatus

import pytest

from src.core.models import UserRoleEnum


class TestCreateUser:
    @pytest.mark.asyncio
    async def test_list_users_successful(self, client, admin_token, admin_payload):
        test_token = await admin_token()
        header = {"Authorization": f"Bearer {test_token}"}
        response = await client.get(url="/api/v1/users/", headers=header)
        assert response.status_code == HTTPStatus.OK
        assert response.json() == [
            {
                "id": 1,
                "role": UserRoleEnum.Admin.value,
                "username": admin_payload["username"],
                "first_name": None,
                "last_name": None,
                "is_active": True,
            }
        ]
