from uuid import UUID

from pydantic import BaseModel, Field


class UUIDMixin(BaseModel):
    id: UUID = Field()


class ProfileModel(BaseModel):
    user_id: UUID = Field()
