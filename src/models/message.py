from enum import Enum

from pydantic import BaseModel


class UseCase(str, Enum):
    profile_change = 'PROFILE_CHANGE'
    profile_movie_change = 'PROFILE_MOVIE_CHANGE'


class BrokerMessageModel(BaseModel):
    use_case: str
    payload: dict

    class Config:
        use_enum_values = True
