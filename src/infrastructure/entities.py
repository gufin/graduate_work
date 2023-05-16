from sqlalchemy import UUID, Column, MetaData, String, Boolean
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
