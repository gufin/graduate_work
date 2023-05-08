from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from core.containers import Container
from use_cases.profile_service import ProfileService

router = APIRouter()


@router.post('')
@inject
async def new_profile(
    profile_service: ProfileService = Depends(Provide[Container.profile_service]),
) -> None:
    pass
