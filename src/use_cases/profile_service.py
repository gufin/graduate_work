import typing

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.entities import Profile, engine, UserFavoriteMovies
from absctract_repositories import AbstractStorage

from models.profile import ProfileModel, UserFavoriteMoviesModel


class ProfileService:
    def __init__(self, *, storage: AbstractStorage):
        self.storage = storage

    async def create(self, *, profile: 'ProfileModel'):
        """Создать профиль пользователя"""
        await self.storage.create(data=profile)

    async def update(self, *, user_id: str, profile: 'ProfileModel'):
        """Обновить профиль пользователя"""
        await self.storage.update(user_id=user_id, data=profile)

    async def get(self, user_id: str | None = None):
        """Получить профиль одного пользователя по индефикатору
        или если индефитор пустой показать всех.
        """
        await self.storage.get(user_id=user_id)

    async def delete(self, user_id: str):
        """Заморозить профиль пользователя"""
        await self.storage.delete(user_id=user_id)

    async def favorite_movies_update(self, *,
                                     user_favorite_movies_model: UserFavoriteMoviesModel):
        async with AsyncSession(engine) as session:
            async with session.begin():
                # Поиск записи
                user_favorite_movie = await session.query(
                    UserFavoriteMovies).filter(
                    and_(
                        UserFavoriteMovies.user_id == user_favorite_movies_model.user_id,
                        UserFavoriteMovies.movie_id == user_favorite_movies_model.movie_id,
                    )
                ).first()
                if user_favorite_movie:
                    user_favorite_movie.is_deleted = user_favorite_movies_model.is_deleted
                else:
                    user_favorite_movie = UserFavoriteMovies(
                        user_id=user_favorite_movies_model.user_id,
                        movie_id=user_favorite_movies_model.movie_id,
                        is_deleted=user_favorite_movies_model.is_deleted,
                    )
                    session.add(user_favorite_movie)

                await session.commit()

