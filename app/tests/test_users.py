from httpx import AsyncClient, codes
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.models import User
from app.tests.conftest import (
    default_user_email,
    default_user_id,
    default_user_password_hash,
)


async def test_read_current_user(client: AsyncClient, default_user_headers):
    response = await client.get(
        app.url_path_for("read_current_user"), headers=default_user_headers
    )
    assert response.status_code == codes.OK
    assert response.json() == {
        "id": default_user_id,
        "email": default_user_email,
    }


async def test_delete_current_user(
    client: AsyncClient, default_user_headers, session: AsyncSession
):
    response = await client.delete(
        app.url_path_for("delete_current_user"), headers=default_user_headers
    )
    assert response.status_code == codes.NO_CONTENT
    result = await session.execute(select(User).where(User.id == default_user_id))
    user = result.scalars().first()
    assert user is None


async def test_reset_current_user_password(
    client: AsyncClient, default_user_headers, session: AsyncSession
):
    response = await client.post(
        app.url_path_for("reset_current_user_password"),
        headers=default_user_headers,
        json={"password": "testxxxxxx"},
    )
    assert response.status_code == codes.OK
    result = await session.execute(select(User).where(User.id == default_user_id))
    user = result.scalars().first()
    assert user is not None
    assert user.hashed_password != default_user_password_hash


async def test_register_new_user(
    client: AsyncClient, default_user_headers, session: AsyncSession
):
    response = await client.post(
        app.url_path_for("register_new_user"),
        headers=default_user_headers,
        json={
            "email": "qwe@example.com",
            "password": "asdasdasd",
        },
    )
    assert response.status_code == codes.OK
    result = await session.execute(select(User).where(User.email == "qwe@example.com"))
    user = result.scalars().first()
    assert user is not None


async def test_update_current_user(
    client: AsyncClient, default_user_headers, session: AsyncSession
):
    response = await client.patch(
        app.url_path_for("update_user"),
        headers=default_user_headers,
        json={
            "first_name": "qwe",
            "last_name": "qwe",
            "mobile_number": "qwe",
            "road": "qwe",
            "city": "qwe",
            "state": "qwe",
            "zip": "qwe",
            "country": "qwe",
            "phone_number": "qwe",
        },
    )
    assert response.status_code == codes.OK
    result = await session.execute(select(User).where(User.id == default_user_id))
    user = result.scalars().first()
    assert user is not None
    assert user.first_name == "qwe"
    assert user.last_name == "qwe"
    assert user.mobile_number == "qwe"
    assert user.road == "qwe"
    assert user.city == "qwe"
    assert user.state == "qwe"
    assert user.zip == "qwe"
    assert user.country == "qwe"
    assert user.phone_number == "qwe"


async def test_version(
    client: AsyncClient, default_user_headers, session: AsyncSession
):
    response = await client.patch(
        app.url_path_for("update_user"),
        headers=default_user_headers,
        json={"version": 1},
    )
    assert response.status_code == codes.OK
    result = await session.execute(select(User).where(User.id == default_user_id))
    user = result.scalars().first()
    assert user is not None
    assert user.version == 1
