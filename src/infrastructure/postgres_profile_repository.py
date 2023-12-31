import logging
import uuid

from sqlalchemy import and_, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.entities import Profile, ProfileMovie, engine
from models.profile import (
    ProfileCreateModel,
    ProfileMovieReadModel,
    ProfileMovieUpdateModel,
    ProfileReadModel,
    ProfileUpdateModel,
)
from use_cases.abstract_repositories import AbstractProfileRepository


class PostgresProfileRepository(AbstractProfileRepository):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def create(self, *, user_id: str, create_model: ProfileCreateModel) -> ProfileReadModel:
        self.logger.info('Creating profile for user_id: %s', user_id)
        profile_result_model = ProfileReadModel(
            id=uuid.uuid4(),
            user_id=user_id,
            is_active=True,
            **create_model.dict(),
        )
        async with AsyncSession(engine) as session:
            async with session.begin():
                session.add(Profile(**profile_result_model.dict()))
            await session.commit()
            self.logger.debug('Committing profile creation transaction.')
        return profile_result_model

    async def update(self, *, user_id: str, update_model: ProfileUpdateModel) -> ProfileReadModel:
        self.logger.info('Updating profile for user_id: %s', user_id)
        async with AsyncSession(engine) as session:
            async with session.begin():
                update_result = await session.scalar(
                    update(Profile).where(
                        Profile.user_id == user_id,
                    ).values(
                        **update_model.dict(exclude_none=True),
                    ).returning(Profile),
                )
                update_result_model = self._convert_profile_to_model(profile=update_result)
            await session.commit()
            self.logger.debug('Committing profile update transaction.')

            return update_result_model

    async def read(self, user_id: str) -> ProfileReadModel:
        self.logger.info('Reading profile for user_id: %s', user_id)
        async with AsyncSession(engine) as session:
            async with session.begin():
                read_result: Profile = await session.scalar(select(Profile).where(Profile.user_id == user_id)) # noqa
                if not read_result:
                    raise NoResultFound
                return self._convert_profile_to_model(profile=read_result)

    async def movie_update(self, *, update_model: ProfileMovieUpdateModel) -> ProfileMovieReadModel:
        self.logger.info('Updating movie for user_id: %s', update_model.user_id)
        async with AsyncSession(engine) as session:
            async with session.begin():
                profile: Profile = await session.scalar(select(Profile).where(
                    Profile.user_id == update_model.user_id,
                ))
                if update_model.is_deleted:
                    profile_movie = await session.scalar(select(ProfileMovie).where(
                        and_(
                            profile.user_id == update_model.user_id,
                            ProfileMovie.movie_id == update_model.movie_id,
                        ),
                    ))
                    await session.delete(profile_movie)
                else:
                    profile_movie = ProfileMovie(
                        id=uuid.uuid4(),
                        profile=profile,
                        movie_id=update_model.movie_id,
                    )
                    session.add(profile_movie)
                update_result = ProfileMovieReadModel(
                    profile_id=profile.id,
                    movie_id=update_model.movie_id,
                    is_deleted=update_model.is_deleted,
                )

            await session.commit()
            self.logger.debug('Movie updated for user_id: %s', update_model.user_id)
            return update_result

    async def get_favorite_movie_ids(self, *, user_id: str) -> list[str]:
        self.logger.info('Getting users favorite movies for user_id: %s', user_id)
        async with AsyncSession(engine) as session:
            async with session.begin():
                profile: Profile = await session.scalar(select(Profile).where(
                    Profile.user_id == user_id,
                ))
                movies = await session.execute(select(ProfileMovie).where(ProfileMovie.profile == profile)) # noqa
                return [row[0].movie_id for row in movies.all()]

    @staticmethod
    def _convert_profile_to_model(profile: Profile) -> ProfileReadModel:
        return ProfileReadModel(
            id=profile.id,
            user_id=profile.user_id,
            first_name=profile.first_name,
            last_name=profile.last_name,
            patronymic=profile.patronymic,
            phone=profile.phone,
            is_active=profile.is_active,
        )
