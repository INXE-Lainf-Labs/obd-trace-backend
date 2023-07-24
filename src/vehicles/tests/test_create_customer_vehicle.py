from http import HTTPStatus

import pytest

import json


class TestCreateCustomerVehicle:
    @pytest.mark.asyncio
    async def test_create_customer_vehicle_with_existent_vehicle_successfully(
        self, client, vehicle, customer, vehicle_payload, admin_token
    ):
        test_customer = await customer()
        test_token = await admin_token()
        customer_vehicle_payload = {
            "vin": "TESTVIN1234",
            "plate_code": "",
            "customer_id": test_customer.id,
        }
        payload = json.dumps(customer_vehicle_payload)
        header = {"Authorization": f"Bearer {test_token}"}
        response = await client.post(
            url=f"/api/v1/vehicles/customer/{vehicle_payload['id']}",
            data=payload,
            headers=header,
        )
        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {
            "vin": customer_vehicle_payload["vin"],
            "plate_code": customer_vehicle_payload["plate_code"],
            "customer_id": customer_vehicle_payload["customer_id"],
            "vehicle_id": vehicle_payload["id"],
        }

    @pytest.mark.asyncio
    async def test_user_not_found_on_creating_customer_vehicle(
        self, client, vehicle, vehicle_payload, admin_token
    ):
        test_token = await admin_token()
        customer_vehicle_payload = {
            "vin": "TESTVIN1234",
            "plate_code": "",
            "customer_id": 2,
        }
        payload = json.dumps(customer_vehicle_payload)
        header = {"Authorization": f"Bearer {test_token}"}
        response = await client.post(
            url=f"/api/v1/vehicles/customer/{vehicle_payload['id']}",
            data=payload,
            headers=header,
        )
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {"detail": "Customer not found for given id."}

    @pytest.mark.asyncio
    async def test_vehicle_not_found_on_creating_customer_vehicle(
        self, client, customer, vehicle_payload, admin_token
    ):
        test_customer = await customer()
        test_token = await admin_token()
        customer_vehicle_payload = {
            "vin": "TESTVIN1234",
            "plate_code": "",
            "customer_id": test_customer.id,
        }
        payload = json.dumps(customer_vehicle_payload)
        header = {"Authorization": f"Bearer {test_token}"}
        response = await client.post(
            url=f"/api/v1/vehicles/customer/{vehicle_payload['id']}",
            data=payload,
            headers=header,
        )
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {"detail": "Vehicle not found for given vehicle_id"}

    @pytest.mark.asyncio
    async def test_create_customer_vehicle_with_new_vehicle_successfully(
        self, client, customer, vehicle_payload, admin_token
    ):
        test_customer = await customer()
        test_token = await admin_token()
        customer_vehicle_payload = {
            "vin": "TESTVIN1234",
            "plate_code": "",
            "customer_id": test_customer.id,
            **vehicle_payload,
        }
        payload = json.dumps(customer_vehicle_payload)
        header = {"Authorization": f"Bearer {test_token}"}
        response = await client.post(
            url=f"/api/v1/vehicles/customer/", data=payload, headers=header
        )
        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {
            "vin": customer_vehicle_payload["vin"],
            "plate_code": customer_vehicle_payload["plate_code"],
            "customer_id": customer_vehicle_payload["customer_id"],
            "vehicle_id": vehicle_payload["id"],
        }

    @pytest.mark.asyncio
    async def test_bad_request_on_creating_customer_vehicle_with_new_vehicle(
        self, client, customer, vehicle, vehicle_payload, admin_token
    ):
        test_customer = await customer()
        test_token = await admin_token()
        customer_vehicle_payload = {
            "vin": "TESTVIN1234",
            "plate_code": "",
            "customer_id": test_customer.id,
            **vehicle_payload,
        }
        payload = json.dumps(customer_vehicle_payload)
        header = {"Authorization": f"Bearer {test_token}"}
        response = await client.post(
            url=f"/api/v1/vehicles/customer/", data=payload, headers=header
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {
            "detail": f"Vehicle already exists with id {vehicle_payload['id']}"
        }
