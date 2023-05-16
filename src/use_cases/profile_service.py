import typing

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.entities import Profile, engine


if typing.TYPE_CHECKING:
    from models.profile import ProfileModel


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
