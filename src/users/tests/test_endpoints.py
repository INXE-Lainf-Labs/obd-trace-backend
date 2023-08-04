import json
from http import HTTPStatus

import pytest


class TestUsersEndpoints:
    @pytest.mark.asyncio
    async def test_list_users_successfully(
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

    @pytest.mark.asyncio
    async def test_create_customer_successfully(
        self, client, customer_role, user_payload, admin_token
    ):
        test_token = await admin_token()
        header = {"Authorization": f"Bearer {test_token}"}
        response = await client.post(
            url="/api/v1/users/customer/", data=user_payload, headers=header
        )
        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {
            "id": 2,
            "role": customer_role,
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
    async def test_create_employee_successfully(
        self, client, user_payload, admin_token
    ):
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

    @pytest.mark.asyncio
    async def test_update_customer_successfully(self, client, user_payload, user_token):
        test_token = await user_token()
        header = {"Authorization": f"Bearer {test_token}"}
        customer_payload = {
            "username": user_payload["username"],
            # "password": user_payload["password"],
            "first_name": "John",
            "last_name": "Doe",
            "address": {
                "street": "Street",
                "city": "City",
                "state": "State",
                "complement": "Complement",
                "zipcode": "Zip Code",
            },
        }
        payload = json.dumps(customer_payload)

        response = await client.put(
            url="/api/v1/users/customer/1/", data=payload, headers=header
        )
        print(response.json())
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            "id": 1,
            "username": user_payload["username"],
            "first_name": "John",
            "last_name": "Doe",
            "is_active": True,
            "role": "CUSTOMER",
        }

    @pytest.mark.asyncio
    async def test_get_customers_successfully(self, client, customers, admin_token):
        test_token = await admin_token()
        customer1, customer2 = customers
        header = {"Authorization": f"Bearer {test_token}"}

        response = await client.get(url="/api/v1/users/customers/", headers=header)
        print(response.json())
        assert response.status_code == HTTPStatus.OK
        assert response.json() == [
            {
                "username": customer1["username"],
                "first_name": customer1["first_name"],
                "last_name": customer1["last_name"],
                "is_active": customer1["is_active"],
                "role": customer1["role"],
                "street": customer1["street"],
                "city": customer1["city"],
                "state": customer1["state"],
                "complement": customer1["complement"],
                "zipcode": customer1["zipcode"],
            },
            {
                "username": customer2["username"],
                "first_name": customer2["first_name"],
                "last_name": customer2["last_name"],
                "is_active": customer1["is_active"],
                "role": customer1["role"],
                "street": customer2["street"],
                "city": customer2["city"],
                "state": customer2["state"],
                "complement": customer2["complement"],
                "zipcode": customer2["zipcode"],
            },
        ]
