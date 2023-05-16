import typing

from sqlalchemy import and_, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.entities import Profile, engine, UserFavoriteMovies

from models.profile import ProfileModel, UserFavoriteMoviesModel


class ProfileService:
    async def create(self, *, profile: 'ProfileModel'):
        """Создать профиль пользователя"""
        prfile_data = Profile(**profile.dict())
        async with AsyncSession(engine) as session:
            async with session.begin():
                session.add(prfile_data)
            await session.commit()
        return str(profile.user_id)

    async def update(self, *, user_id: str, profile: 'ProfileModel'):
        """Обновить профиль пользователя"""
        async with AsyncSession(engine) as session:
            async with session.begin():
                await session.execute(
                    update(Profile)
                    .where(Profile.user_id == user_id)
                    .values(**profile.dict())
                )
            await session.commit()

    async def get(self, user_id: str | None = None):
        """Получить профиль одного пользователя по индефикатору
        или если индефитор пустой показать всех.
        """
        async with AsyncSession(engine) as session:
            async with session.begin():
                if user_id:
                    query = await session.execute(select(Profile).where(Profile.user_id == user_id))
                else:
                    query = await session.execute(select(Profile))
                return query.all()

    async def delete(self, user_id: str):
        """Заморозить профиль пользователя"""
        async with AsyncSession(engine) as session:
            async with session.begin():
                await session.execute(delete(Profile).where(Profile.user_id == user_id))
            await session.commit()

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

