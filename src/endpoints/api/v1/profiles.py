from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from core.containers import Container
from models.profile import ProfileCreateModel, ProfileReadModel, ProfileUpdateModel
from use_cases.profile_service import ProfileService

router = APIRouter()


@router.post('/{user_id}')
@inject
async def new_profile(
    user_id: str,
    profile_create_model: ProfileCreateModel,
    profile_service: ProfileService = Depends(Provide[Container.profile_service]),
) -> ProfileReadModel:
    return await profile_service.create(user_id=user_id, profile_model=profile_create_model)


@router.get('/{user_id}')
@inject
async def read_profile(
    user_id: str,
    profile_service: ProfileService = Depends(Provide[Container.profile_service]),
) -> ProfileReadModel:
    return await profile_service.get(user_id=user_id)


@router.put('/{user_id}')
@inject
async def update_profile(
    user_id: str,
    update_model: ProfileUpdateModel,
    profile_service: ProfileService = Depends(Provide[Container.profile_service]),
) -> ProfileReadModel:
    return await profile_service.update(user_id=user_id, update_model=update_model)


@router.delete('/{user_id}')
@inject
async def deactivate_profile(
    user_id: str,
    profile_service: ProfileService = Depends(Provide[Container.profile_service]),
) -> ProfileReadModel:
    return await profile_service.deactivate(user_id=user_id)
