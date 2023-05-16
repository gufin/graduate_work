from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from core.containers import Container
from use_cases.profile_service import ProfileService
from models.profile import ProfileModel

router = APIRouter()


@router.post('/')
@inject
async def new_profile(
    profile: ProfileModel,
    profile_service: ProfileService = Depends(Provide[Container.profile_service]),
) -> dict:
    user_id = await profile_service.create(profile=profile)
    return {'user_id': user_id}


@router.get('/')
@inject
async def get_profile(
        profile_service: ProfileService = Depends(Provide[Container.profile_service]),
) -> list:
    result = await profile_service.get()
    return result


@router.get('/{user_id}')
@inject
async def get_one_profile(
        user_id: str,
        profile_service: ProfileService = Depends(Provide[Container.profile_service]),
) -> list:
    result = await profile_service.get(user_id=user_id)
    return result


@router.put('/{user_id}')
@inject
async def update_profile(
        user_id: str,
        profile: ProfileModel,
        profile_service: ProfileService = Depends(Provide[Container.profile_service]),
) -> None:
    await profile_service.update(user_id=user_id, profile=profile)


@router.delete('/{user_id}')
@inject
async def freezee_profile(
        user_id: str,
        profile_service: ProfileService = Depends(Provide[Container.profile_service]),
) -> None:
    await profile_service.delete(user_id=user_id)
