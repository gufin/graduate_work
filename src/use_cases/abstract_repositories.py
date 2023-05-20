from abc import ABCMeta, abstractmethod

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
    async def get_favorite_movie_ids(self, *, user_id: str) -> list:
        pass
