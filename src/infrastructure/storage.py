from sqlalchemy import and_, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from use_cases.absctract_repositories import AbstractStorage
from models.profile import ProfileModel
from infrastructure.entities import Profile, engine


class PostgreStorage(AbstractStorage):
    async def create(self, data: ProfileModel):
        prfile_data = Profile(**data.dict())
        async with AsyncSession(engine) as session:
            async with session.begin():
                session.add(prfile_data)
            await session.commit()
        return str(data.user_id)
    
    async def update(self, *, user_id: str, data: 'ProfileModel'):
        """Обновить профиль пользователя"""
        async with AsyncSession(engine) as session:
            async with session.begin():
                await session.execute(
                    update(Profile)
                    .where(Profile.user_id == user_id)
                    .values(**data.dict())
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
