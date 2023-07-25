import json
from http import HTTPStatus

import pytest
from sqlmodel import select

from src.services.models import Service


class TestServicesEndpoint:
    @pytest.mark.asyncio
    async def test_list_services_successfully(self, client, service, service_payload):
        response = await client.get(url="/api/v1/services/")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == [
            {
                "id": service_payload["id"],
                "name": service_payload["name"],
                "price": service_payload["price"],
                "description": service_payload["description"],
                "image": service_payload["image"],
                "estimated_time": service_payload["estimated_time"],
                "category": service_payload["category"],
            },
        ]

    @pytest.mark.asyncio
    async def test_get_service_by_id_successfully(
        self, client, service, service_payload
    ):
        response = await client.get(url=f"/api/v1/services/{service_payload['id']}/")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            "id": service_payload["id"],
            "name": service_payload["name"],
            "price": service_payload["price"],
            "description": service_payload["description"],
            "image": service_payload["image"],
            "estimated_time": service_payload["estimated_time"],
            "category": service_payload["category"],
        }

    @pytest.mark.asyncio
    async def test_create_service_successfully(
        self, client, service_payload, admin_token
    ):
        test_token = await admin_token()
        headers = {"Authorization": f"Bearer {test_token}"}
        payload = json.dumps(service_payload)
        response = await client.post(
            url="/api/v1/services/", data=payload, headers=headers
        )
        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {
            "id": service_payload["id"],
            "name": service_payload["name"],
            "price": service_payload["price"],
            "description": service_payload["description"],
            "image": service_payload["image"],
            "estimated_time": service_payload["estimated_time"],
            "category": service_payload["category"],
        }

    @pytest.mark.asyncio
    async def test_create_service_with_unauthorized_user(
        self, client, service_payload, user_token
    ):
        test_token = await user_token()
        headers = {"Authorization": f"Bearer {test_token}"}
        payload = json.dumps(service_payload)
        response = await client.post(
            url="/api/v1/services/", data=payload, headers=headers
        )
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.json() == {
            "detail": "Token bearer cannot execute the required operation"
        }

    @pytest.mark.asyncio
    async def test_create_service_with_expired_token(
        self, client, service_payload, expired_token
    ):
        test_token = await expired_token()
        headers = {"Authorization": f"Bearer {test_token}"}
        payload = json.dumps(service_payload)
        response = await client.post(
            url="/api/v1/services/", data=payload, headers=headers
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "Invalid token"}

    @pytest.mark.asyncio
    async def test_update_service_successfully(
        self, client, service, service_payload, admin_token, db_session
    ):
        test_token = await admin_token()
        headers = {"Authorization": f"Bearer {test_token}"}
        updated_service_payload = service_payload.copy()
        updated_service_payload["name"] = "test update service"
        updated_service_payload["price"] = 150.00
        payload = json.dumps(updated_service_payload)

        response = await client.put(
            url=f"/api/v1/services/{service_payload['id']}/",
            data=payload,
            headers=headers,
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            "id": service_payload["id"],
            "name": updated_service_payload["name"],
            "price": updated_service_payload["price"],
            "description": service_payload["description"],
            "image": service_payload["image"],
            "estimated_time": service_payload["estimated_time"],
            "category": service_payload["category"],
        }

        result = await db_session.execute(
            select(Service).where(Service.id == updated_service_payload["id"])
        )
        updated_service = result.scalar_one_or_none()
        assert updated_service.name == updated_service_payload["name"]
        assert updated_service.price == updated_service_payload["price"]
        assert updated_service.description == updated_service_payload["description"]

    @pytest.mark.asyncio
    async def test_update_nonexistent_service(
        self, client, service_payload, admin_token
    ):
        test_token = await admin_token()
        headers = {"Authorization": f"Bearer {test_token}"}
        updated_service = service_payload.copy()
        updated_service["name"] = "test update service"
        updated_service["price"] = 150.00
        payload = json.dumps(updated_service)

        response = await client.put(
            url=f"/api/v1/services/{service_payload['id']}/",
            data=payload,
            headers=headers,
        )
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {"detail": "Service not found for given service_id"}

    @pytest.mark.asyncio
    async def test_delete_service_successfully(
        self, client, service, service_payload, admin_token, db_session
    ):
        test_token = await admin_token()
        headers = {"Authorization": f"Bearer {test_token}"}

        response = await client.delete(
            url=f"/api/v1/services/{service_payload['id']}/", headers=headers
        )
        assert response.status_code == HTTPStatus.OK

        result = await db_session.execute(
            select(Service).where(Service.id == service_payload["id"])
        )
        assert result.scalar_one_or_none() is None
