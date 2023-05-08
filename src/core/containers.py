from dependency_injector import containers, providers

from use_cases.profile_service import ProfileService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    profile_service = providers.Factory(ProfileService)
