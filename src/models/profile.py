import uuid

from pydantic import BaseModel


class UUIDMixin(BaseModel):
    id: uuid.UUID


class ProfileReadModel(UUIDMixin):
    user_id: uuid.UUID
    first_name: str
    last_name: str
    patronymic: str
    phone: str
    is_active: bool


class ProfileCreateModel(BaseModel):
    first_name: str
    last_name: str
    patronymic: str | None
    phone: str


class ProfileUpdateModel(BaseModel):
    first_name: str | None
    last_name: str | None
    patronymic: str | None
    phone: str | None
    is_active: bool | None


class ProfileMovieUpdateModel(BaseModel):
    user_id: uuid.UUID
    movie_id: uuid.UUID
    is_deleted: bool = False


class ProfileMovieReadModel(BaseModel):
    profile_id: uuid.UUID
    movie_id: uuid.UUID
    is_deleted: bool
