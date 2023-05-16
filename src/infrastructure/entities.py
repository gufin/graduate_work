from sqlalchemy import UUID, Column, MetaData, String, Boolean, UniqueConstraint
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from core.settings import settings

engine = create_async_engine(settings.postgres_url, echo=True)
Base = declarative_base(metadata=MetaData(schema=settings.schema_name))
metadata = Base.metadata


class Profile(Base):
    __tablename__ = 'profiles'

    user_id = Column(UUID, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    patronymic = Column(String(255))
    is_active = Column(Boolean, default=True)


class UserFavoriteMovies(Base):
    __tablename__ = 'user_favorite_movies'
    __table_args__ = (UniqueConstraint('user_id', 'movie_id'),)

    id = Column(UUID, primary_key=True)
    user_id = Column(UUID)
    movie_id = Column(UUID)
    is_deleted = Column(Boolean, default=False)
