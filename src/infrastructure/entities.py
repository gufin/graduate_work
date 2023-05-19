from sqlalchemy import UUID, Boolean, Column, ForeignKey, MetaData, String, UniqueConstraint
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from core.settings import settings

engine = create_async_engine(settings.postgres_url, echo=True)
Base = declarative_base(metadata=MetaData(schema=settings.schema_name))
metadata = Base.metadata

MAX_STRING_LENGTH = 255
MAX_PHONE_LENGTH = 15


class Profile(Base):
    __tablename__ = 'profiles'
    __table_args__ = (UniqueConstraint('id', 'user_id'),)

    id = Column(UUID, primary_key=True)
    user_id = Column(UUID)
    first_name = Column(String(MAX_STRING_LENGTH))
    last_name = Column(String(MAX_STRING_LENGTH))
    patronymic = Column(String(MAX_STRING_LENGTH))
    phone = Column(String(MAX_PHONE_LENGTH))
    is_active = Column(Boolean, default=True)
    movie = relationship('ProfileMovie', back_populates='profile')


class ProfileMovie(Base):
    __tablename__ = 'profile_movies'
    __table_args__ = (UniqueConstraint('profile_id', 'movie_id'),)

    id = Column(UUID, primary_key=True)
    movie_id = Column(UUID)
    profile_id = Column(UUID, ForeignKey('profiles.id'))
    profile = relationship('Profile', back_populates='movie', cascade='all,delete')
