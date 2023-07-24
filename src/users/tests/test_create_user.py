import json
from http import HTTPStatus

import pytest

from src.core.models import UserRoleEnum


class TestCreateUser:
    @pytest.mark.asyncio
    async def test_create_customer_successful(self, client, user_payload, admin_token):
        test_token = await admin_token()
        header = {"Authorization": f"Bearer {test_token}"}
        response = await client.post(
            url="/api/v1/users/customer/", data=user_payload, headers=header
        )
        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {
            "id": 2,
            "role": UserRoleEnum.Customer.value,
            "username": user_payload["username"],
        }

    @pytest.mark.asyncio
    async def test_create_existent_user(
        self, client, customer, user_payload, admin_token
    ):
        await customer()
        test_token = await admin_token()
        header = {"Authorization": f"Bearer {test_token}"}
        response = await client.post(
            url="/api/v1/users/customer/", data=user_payload, headers=header
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

    @pytest.mark.asyncio
    async def test_create_user_with_invalid_jwt(self, client, customer, user_payload):
        await customer()
        test_token = "fake_token"
        header = {"Authorization": f"Bearer {test_token}"}
        response = await client.post(
            url="/api/v1/users/customer/", data=user_payload, headers=header
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED

        data = json.loads(response.content)
        assert data["detail"] == "Invalid token"

    @pytest.mark.asyncio
    async def test_create_user_with_expired_jwt(
        self, client, user_payload, expired_token
    ):
        test_token = await expired_token()
        header = {"Authorization": f"Bearer {test_token}"}
        response = await client.post(
            url="/api/v1/users/customer/", data=user_payload, headers=header
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED

        data = json.loads(response.content)
        assert data["detail"] == "Invalid token"

    @pytest.mark.asyncio
    async def test_create_user_with_forbidden_user(
        self, client, user2_payload, user_token
    ):
        test_token = await user_token()
        header = {"Authorization": f"Bearer {test_token}"}
        response = await client.post(
            url="/api/v1/users/customer/", data=user2_payload, headers=header
        )
        assert response.status_code == HTTPStatus.FORBIDDEN

        data = json.loads(response.content)
        assert data["detail"] == "Token bearer cannot execute the required operation"

    @pytest.mark.asyncio
    async def test_create_employee_successful(self, client, user_payload, admin_token):
        test_token = await admin_token()
        header = {"Authorization": f"Bearer {test_token}"}
        response = await client.post(
            url="/api/v1/users/employee/", data=user_payload, headers=header
        )
        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {
            "id": 2,
            "username": user_payload["username"],
        }
