from http import HTTPStatus

import pytest

import json


class TestCreateVehicle:
    @pytest.mark.asyncio
    async def test_create_vehicle_successful(
        self, client, vehicle_payload, admin_token
    ):
        test_token = await admin_token()
        payload = json.dumps(vehicle_payload)
        header = {"Authorization": f"Bearer {test_token}"}
        response = await client.post(
            url="/api/v1/vehicles/", data=payload, headers=header
        )
        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {
            "id": 1,
            "brand": vehicle_payload["brand"],
            "model": vehicle_payload["model"],
            "color": vehicle_payload["color"],
            "year": vehicle_payload["year"],
        }

    @pytest.mark.asyncio
    async def test_create_existent_vehicle(
        self, client, vehicle, vehicle_payload, admin_token
    ):
        payload = json.dumps(vehicle_payload)
        test_token = await admin_token()
        header = {"Authorization": f"Bearer {test_token}"}
        response = await client.post(
            url="/api/v1/vehicles/", data=payload, headers=header
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        data = json.loads(response.content)
        assert (
            data["detail"] == f"Vehicle already exists with id {vehicle_payload['id']}"
        )

    @pytest.mark.asyncio
    async def test_create_vehicle_with_invalid_jwt(
        self,
        client,
        vehicle_payload,
    ):
        payload = json.dumps(vehicle_payload)
        test_token = "fake_token"
        header = {"Authorization": f"Bearer {test_token}"}
        response = await client.post(
            url="/api/v1/vehicles/", data=payload, headers=header
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED

        data = json.loads(response.content)
        assert data["detail"] == "Invalid token"

    @pytest.mark.asyncio
    async def test_create_vehicle_with_expired_jwt(
        self, client, vehicle_payload, expired_token
    ):
        payload = json.dumps(vehicle_payload)
        test_token = await expired_token()
        header = {"Authorization": f"Bearer {test_token}"}
        response = await client.post(
            url="/api/v1/vehicles/", data=payload, headers=header
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED

        data = json.loads(response.content)
        assert data["detail"] == "Invalid token"

    @pytest.mark.asyncio
    async def test_create_vehicle_with_forbidden_user(
        self, client, vehicle_payload, user_token
    ):
        payload = json.dumps(vehicle_payload)
        test_token = await user_token()
        header = {"Authorization": f"Bearer {test_token}"}
        response = await client.post(
            url="/api/v1/vehicles/", data=payload, headers=header
        )
        assert response.status_code == HTTPStatus.FORBIDDEN

        data = json.loads(response.content)
        assert data["detail"] == "Token bearer cannot execute the required operation"

    #
    # @pytest.mark.asyncio
    # async def test_create_employee_successful(self, client, user_payload, admin_token):
    #     test_token = await admin_token()
    #     header = {"Authorization": f"Bearer {test_token}"}
    #     response = await client.post(
    #         url="/api/v1/users/employee/", data=user_payload, headers=header
    #     )
    #     assert response.status_code == HTTPStatus.CREATED
    #     assert response.json() == {
    #         "id": 2,
    #         "username": user_payload["username"],
    #     }
