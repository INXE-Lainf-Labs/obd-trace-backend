import json
from http import HTTPStatus

import pytest
from sqlmodel import select

from src.orders.models import Order
from src.orders.services import get_orders_status_values


class TestServicesEndpoint:
    @pytest.mark.asyncio
    @pytest.mark.freeze_time("2023-07-28")
    async def test_list_orders_successfully(self, client, order, order_payload):
        response = await client.get(url="/api/v1/orders/")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == [
            {
                "id": order_payload["id"],
                "customer_id": order_payload["customer_id"],
                "customer_vehicle_ids": order_payload["customer_vehicle_ids"],
                "service_ids": order_payload["service_ids"],
                "employee_ids": order_payload["employee_ids"],
                "start_date": order_payload["start_date"].isoformat(),
                "estimated_time": order_payload["estimated_time"].isoformat(),
                "status": order_payload["status"],
            },
        ]

    @pytest.mark.asyncio
    async def test_get_order_by_id_successfully(self, client, order, order_payload):
        response = await client.get(url=f"/api/v1/orders/{order_payload['id']}/")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            "id": order_payload["id"],
            "customer_id": order_payload["customer_id"],
            "customer_vehicle_ids": order_payload["customer_vehicle_ids"],
            "service_ids": order_payload["service_ids"],
            "employee_ids": order_payload["employee_ids"],
            "start_date": order_payload["start_date"].isoformat(),
            "estimated_time": order_payload["estimated_time"].isoformat(),
            "status": order_payload["status"],
        }

    @pytest.mark.asyncio
    @pytest.mark.freeze_time("2023-07-28")
    async def test_create_order_successfully(
        self, client, order_payload, customer, admin_token
    ):
        test_token = await admin_token()
        test_customer = await customer()
        headers = {"Authorization": f"Bearer {test_token}"}
        updated_order_payload = order_payload.copy()
        updated_order_payload["customer_id"] = test_customer.id
        updated_order_payload["start_date"] = order_payload["start_date"].isoformat()
        updated_order_payload["estimated_time"] = order_payload[
            "estimated_time"
        ].isoformat()
        payload = json.dumps(updated_order_payload)
        response = await client.post(
            url="/api/v1/orders/", data=payload, headers=headers
        )
        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {
            "id": order_payload["id"],
            "customer_id": test_customer.id,
            "customer_vehicle_ids": order_payload["customer_vehicle_ids"],
            "service_ids": order_payload["service_ids"],
            "employee_ids": order_payload["employee_ids"],
            "start_date": order_payload["start_date"].isoformat(),
            "estimated_time": order_payload["estimated_time"].isoformat(),
            "status": order_payload["status"],
        }

    @pytest.mark.asyncio
    async def test_create_order_with_unauthorized_user(
        self, client, order_payload, user_token
    ):
        test_token = await user_token()
        headers = {"Authorization": f"Bearer {test_token}"}
        updated_order_payload = order_payload.copy()
        updated_order_payload["start_date"] = order_payload["start_date"].isoformat()
        updated_order_payload["estimated_time"] = order_payload[
            "estimated_time"
        ].isoformat()
        payload = json.dumps(updated_order_payload)
        response = await client.post(
            url="/api/v1/orders/", data=payload, headers=headers
        )
        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.json() == {
            "detail": "Token bearer cannot execute the required operation"
        }

    @pytest.mark.asyncio
    async def test_create_order_with_expired_token(
        self, client, order_payload, expired_token
    ):
        test_token = await expired_token()
        headers = {"Authorization": f"Bearer {test_token}"}
        updated_order_payload = order_payload.copy()
        updated_order_payload["start_date"] = order_payload["start_date"].isoformat()
        updated_order_payload["estimated_time"] = order_payload[
            "estimated_time"
        ].isoformat()
        payload = json.dumps(updated_order_payload)
        response = await client.post(
            url="/api/v1/orders/", data=payload, headers=headers
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "Invalid token"}

    @pytest.mark.asyncio
    async def test_update_order_successfully(
        self, client, order, order_payload, admin_token, db_session
    ):
        status = get_orders_status_values()
        test_token = await admin_token()
        headers = {"Authorization": f"Bearer {test_token}"}

        updated_order_payload = order_payload.copy()
        updated_order_payload["start_date"] = order_payload["start_date"].isoformat()
        updated_order_payload["estimated_time"] = order_payload[
            "estimated_time"
        ].isoformat()
        updated_order_payload["status"] = status[1]
        payload = json.dumps(updated_order_payload)

        response = await client.put(
            url=f"/api/v1/orders/{order_payload['id']}/",
            data=payload,
            headers=headers,
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            "id": order_payload["id"],
            "customer_id": updated_order_payload["customer_id"],
            "customer_vehicle_ids": order_payload["customer_vehicle_ids"],
            "service_ids": updated_order_payload["service_ids"],
            "employee_ids": updated_order_payload["employee_ids"],
            "start_date": updated_order_payload["start_date"],
            "estimated_time": updated_order_payload["estimated_time"],
            "status": updated_order_payload["status"],
        }

        result = await db_session.execute(
            select(Order).where(Order.id == updated_order_payload["id"])
        )
        updated_order = result.scalar_one_or_none()
        assert updated_order.status == updated_order_payload["status"]

    @pytest.mark.asyncio
    async def test_fail_on_update_nonexistent_order(
        self, client, order_payload, admin_token
    ):
        status = get_orders_status_values()
        test_token = await admin_token()
        headers = {"Authorization": f"Bearer {test_token}"}

        updated_order_payload = order_payload.copy()
        updated_order_payload["start_date"] = order_payload["start_date"].isoformat()
        updated_order_payload["estimated_time"] = order_payload[
            "estimated_time"
        ].isoformat()
        updated_order_payload["status"] = status[1]
        payload = json.dumps(updated_order_payload)

        response = await client.put(
            url=f"/api/v1/orders/{order_payload['id']}/",
            data=payload,
            headers=headers,
        )
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {"detail": "Service not found for given service_id"}

    @pytest.mark.asyncio
    async def test_delete_order_successfully(
        self, client, order, order_payload, admin_token, db_session
    ):
        test_token = await admin_token()
        headers = {"Authorization": f"Bearer {test_token}"}

        response = await client.delete(
            url=f"/api/v1/orders/{order_payload['id']}/", headers=headers
        )
        assert response.status_code == HTTPStatus.OK

        result = await db_session.execute(
            select(Order).where(Order.id == order_payload["id"])
        )
        assert result.scalar_one_or_none() is None

    @pytest.mark.asyncio
    async def test_fail_delete_nonexistent_order(
        self, client, order_payload, admin_token
    ):
        test_token = await admin_token()
        headers = {"Authorization": f"Bearer {test_token}"}

        response = await client.delete(
            url=f"/api/v1/orders/{order_payload['id']}/", headers=headers
        )
        assert response.status_code == HTTPStatus.NOT_FOUND
