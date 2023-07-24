from http import HTTPStatus

import pytest


class TestGetVehicles:
    @pytest.mark.asyncio
    async def test_list_vehicles_successful(self, client, vehicle, vehicle_payload):
        response = await client.get(url="/api/v1/vehicles/")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == [
            {
                "id": vehicle_payload["id"],
                "brand": vehicle_payload["brand"],
                "model": vehicle_payload["model"],
                "color": vehicle_payload["color"],
                "year": vehicle_payload["year"],
            },
        ]

    @pytest.mark.asyncio
    async def test_get_vehicle_by_id_successful(self, client, vehicle, vehicle_payload):
        response = await client.get(url=f"/api/v1/vehicles/{vehicle_payload['id']}/")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            "id": vehicle_payload["id"],
            "brand": vehicle_payload["brand"],
            "model": vehicle_payload["model"],
            "color": vehicle_payload["color"],
            "year": vehicle_payload["year"],
        }
