import uuid

from sqlalchemy import and_, select, update
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
    async def create(self, *, user_id: str, create_model: ProfileCreateModel) -> ProfileReadModel:
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
        return profile_result_model

    async def update(self, *, user_id: str, update_model: ProfileUpdateModel) -> ProfileReadModel:
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

            return update_result_model

    async def read(self, user_id: str) -> ProfileReadModel:
        async with AsyncSession(engine) as session:
            async with session.begin():
                read_result: Profile = await session.scalar(select(Profile).where(Profile.user_id == user_id))
                return self._convert_profile_to_model(profile=read_result)

    async def movie_update(self, *, update_model: ProfileMovieUpdateModel) -> ProfileMovieReadModel:
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
            return update_result

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
