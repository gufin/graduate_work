from abc import ABC, ABCMeta, abstractmethod

from models.profile import (
    ProfileCreateModel,
    ProfileMovieReadModel,
    ProfileMovieUpdateModel,
    ProfileReadModel,
    ProfileUpdateModel,
)


class AbstractProfileRepository(metaclass=ABCMeta):
    @abstractmethod
    async def create(self, *, user_id: str, create_model: ProfileCreateModel) -> ProfileReadModel:
        pass

    @abstractmethod
    async def update(self, *, user_id: str, update_model: ProfileUpdateModel) -> ProfileReadModel:
        pass

    @abstractmethod
    async def read(self, *, user_id: str) -> ProfileReadModel:
        pass

    @abstractmethod
    async def movie_update(self, *, update_model: ProfileMovieUpdateModel) -> ProfileMovieReadModel:
        pass

    @abstractmethod
    async def get_favorite_movie_ids(self, *, user_id: str) -> list: # noqa
        pass


class AbstractAuthRepository(ABC):
    @abstractmethod
    async def verify(self, *, token: str, roles: str, headers: dict) -> bool:
        pass

    @abstractmethod
    async def is_profile_in_group(self, *, group_id: str, user_id: str) -> bool:
        pass


auth_client: AbstractAuthRepository | None = None


def get_auth_client() -> AbstractAuthRepository:
    return auth_client
