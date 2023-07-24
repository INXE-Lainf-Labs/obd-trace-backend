import json
from http import HTTPStatus

import pytest


class TestAuthentication:
    @pytest.mark.asyncio
    async def test_user_signin_successful(self, client, user_payload, customer):
        test_customer = await customer()
        response = await client.post(url="/api/v1/auth/signin/", data=user_payload)
        assert response.status_code == HTTPStatus.OK

        data = json.loads(response.content)
        assert data["id"] == test_customer.id

    @pytest.mark.asyncio
    async def test_user_signin_with_wrong_password(
        self, client, user_payload, customer
    ):
        await customer()
        wrong_user_payload = user_payload.copy()
        wrong_user_payload["password"] = "wrong_password"
        response = await client.post(
            url="/api/v1/auth/signin/", data=wrong_user_payload
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

        data = json.loads(response.content)
        assert data["detail"] == "Incorrect username or password."

    @pytest.mark.asyncio
    async def test_user_signin_with_wrong_username(
        self, client, user_payload, customer
    ):
        await customer()
        wrong_user_payload = user_payload.copy()
        wrong_user_payload["username"] = "wrong.username@email.com"
        response = await client.post(
            url="/api/v1/auth/signin/", data=wrong_user_payload
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

        data = json.loads(response.content)
        assert data["detail"] == "Incorrect username or password."

    @pytest.mark.asyncio
    async def test_user_signup_successful(self, client, user_payload):
        response = await client.post(url="/api/v1/auth/signup/", data=user_payload)
        assert response.status_code == HTTPStatus.CREATED

    @pytest.mark.asyncio
    async def test_user_signup_with_existent_user(self, client, user_payload, customer):
        await customer()
        response = await client.post(url="/api/v1/auth/signup/", data=user_payload)
        assert response.status_code == HTTPStatus.BAD_REQUEST

        data = json.loads(response.content)
        assert data["detail"] == "Username is invalid or already registered"
