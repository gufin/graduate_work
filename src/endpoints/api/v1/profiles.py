from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from core.containers import Container
from use_cases.profile_service import ProfileService

router = APIRouter()


@router.post('/')
@inject
async def new_profile(
    profile_service: ProfileService = Depends(Provide[Container.profile_service]),
) -> None:
    pass


@router.get('/')
@inject
async def get_profile(
        profile_service: ProfileService = Depends(Provide[Container.profile_service]),
) -> None:
    pass


@router.get('/{user_id}')
@inject
async def get_one_profile(
        user_id,
        profile_service: ProfileService = Depends(Provide[Container.profile_service]),
) -> None:
    pass


@router.put('/{user_id}')
@inject
async def update_profile(
        user_id,
        profile_service: ProfileService = Depends(Provide[Container.profile_service]),
) -> None:
    pass


@router.delete('/{user_id}')
@inject
async def freezee_profile(
        user_id,
        profile_service: ProfileService = Depends(Provide[Container.profile_service]),
) -> None:
    pass
