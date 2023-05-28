from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio


async def test_post_profile_valid_data(make_post_request):
    response = await make_post_request(
        '/api/v1/profiles/f970495e-a731-45f0-aa65-686bc6eada23',
        params={
            'first_name': 'TestFirstName',
            'last_name': 'TestLastName',
            'patronymic': 'TestPatronymic',
            'phone': '+1234567890',
        },
    )
    assert response.status == HTTPStatus.OK
    assert response.body == {
        'user_id': 'f970495e-a731-45f0-aa65-686bc6eada23',
        'first_name': 'TestFirstName',
        'last_name': 'TestLastName',
        'patronymic': 'TestPatronymic',
        'phone': '+1234567890',
        'is_active': True,
    }


async def test_post_profile_invalid_data(make_post_request):
    response = await make_post_request(
        '/api/v1/profiles/f970495e-a731-45f0-aa65-686bc6eada23',
        params={
            'first_name': 'TestFirstName',
            'last_name': 'TestLastName',
            'patronymic': 'TestPatronymic',
            'phone': '+1234567890',
        },
    )
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_get_profile_valid_data(make_get_request, create_profile):
    await create_profile
    response = await make_get_request(
        '/api/v1/profiles/f970495e-a731-45f0-aa65-686bc6eada23'
    )
    assert response.status == HTTPStatus.OK
    assert response.body == {
        'user_id': 'f970495e-a731-45f0-aa65-686bc6eada23',
        'first_name': 'TestFirstName',
        'last_name': 'TestLastName',
        'patronymic': 'TestPatronymic',
        'phone': '+1234567890',
        'is_active': True,
    }


async def test_get_profile_invalid_data(make_get_request):
    response = await make_get_request(
        '/api/v1/profiles/f970495e-a731-45f0-aa65-6864c6eada23'
    )
    assert response.status == HTTPStatus.NOT_FOUND


async def test_put_profile_valid_data(make_put_request, create_profile):
    await create_profile
    response = await make_put_request(
        '/api/v1/profiles/f970495e-a731-45f0-aa65-686bc6eada23',
        params={
            'first_name': 'John',
            'last_name': 'Doe',
            'patronymic': 'Smith',
            'phone': '+12345678901',
            'is_active': True,
        },
    )
    assert response.status == HTTPStatus.OK
    assert response.body == {
        'user_id': 'f970495e-a731-45f0-aa65-686bc6eada23',
        'first_name': 'John',
        'last_name': 'Doe',
        'patronymic': 'Smith',
        'phone': '+12345678901',
        'is_active': True,
    }


async def test_put_profile_invalid_data(make_put_request, create_profile):
    await create_profile
    response = await make_put_request(
        '/api/v1/profiles/f970495e-a731-45f0-aa65-686bc6eada23',
        params={
            'first_name': 'John',
            'patronymic': 'Smith',
            'phone': '+12345678901',
            'is_active': True,
        },
    )
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_delete_profile(make_delete_request, create_profile):
    await create_profile
    response = await make_delete_request(
        '/api/v1/profiles/f970495e-a731-45f0-aa65-686bc6eada23'
    )
    assert response.status == HTTPStatus.OK


async def test_delete_profile_invalid_data(make_delete_request, create_profile):
    await create_profile
    response = await make_delete_request(
        '/api/v1/profiles/f970495e-a731-45f0-aa65-676bc6eada23'
    )
    assert response.status == HTTPStatus.NOT_FOUND


async def test_favorite_movie_ids(make_get_request, create_profile, create_test_movies):
    await create_profile
    await create_test_movies
    response = await make_get_request(
        '/api/v1/profiles/f970495e-a731-45f0-aa65-686bc6eada23/favorite_movie_ids'
    )
    assert response.status == HTTPStatus.OK
    assert response.body == [
        '805b3604-b770-46fe-9d25-5d24b4d3a0c2',
        '4322cf42-5dea-43e8-92d4-27316e831b39',
    ]
