import uuid
from typing import Optional

from pydantic import BaseModel, Field


class ProfileModel(BaseModel):
    first_name: str
    last_name: str
    patronymic: Optional[str]
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4)


class UserFavoriteMoviesModel(BaseModel):
    user_id: uuid.UUID
    movie_id: uuid.UUID
    is_deleted: bool = False
