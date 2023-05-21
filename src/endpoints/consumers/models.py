from pydantic import BaseModel


class KafkaMessageModel(BaseModel):
    key: bytes
    value: bytes # noqa
