from http import HTTPStatus

import pytest


class TestGetUser:
    @pytest.mark.asyncio
    async def test_list_users_successful(
        self, client, admin_role, admin_token, admin_payload
    ):
        test_token = await admin_token()
        header = {"Authorization": f"Bearer {test_token}"}
        response = await client.get(url="/api/v1/users/", headers=header)
        assert response.status_code == HTTPStatus.OK
        assert response.json() == [
            {
                "id": 1,
                "role": admin_role,
                "username": admin_payload["username"],
                "first_name": None,
                "last_name": None,
                "is_active": True,
            }
        ]
