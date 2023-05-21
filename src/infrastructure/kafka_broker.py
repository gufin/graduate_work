import json
from collections.abc import Callable
from time import sleep
from typing import Any

from kafka import KafkaConsumer, KafkaProducer
from pydantic import BaseModel

from models.message import BrokerMessageModel, UseCase
from models.profile import ProfileMovieReadModel, ProfileReadModel
from use_cases.abstract_publisher import AbstractPublisher


class KProducer(AbstractPublisher):
    def __init__(self, *, config: dict, topic: str):
        host = config.get('host')
        port = config.get('port')
        self.kafka_producer = KafkaProducer(bootstrap_servers=[f'{host}:{port}'])
        self.topic = topic

    def send(self, *, message: BrokerMessageModel):
        value_model = None
        key = ''
        match message.use_case:
            case UseCase.profile_change.value:
                value_model = ProfileReadModel(**message.payload)
                key = str(value_model.id)
            case UseCase.profile_movie_change:
                value_model = ProfileMovieReadModel(**message.payload)
                key = str(value_model.profile_id)
        self._on_send(model=value_model, key=key)

    def _on_send(self, *, key: str, model: BaseModel = None):
        self.kafka_producer.send(
            self.topic,
            json.dumps(model.json()).encode(),
            key.encode(),
        )


class KConsumer(KafkaConsumer):
    def __init__(self, *topics, process_message: Callable = None, **configs):
        super().__init__(*topics, **configs)
        self.process_message = process_message or self._default_handler
        self._running = False

    @property
    def alive(self):
        return self._running

    def start(self):
        self._running = True

    def stop(self):
        self._running = False

    @staticmethod
    def _default_handler(message: Any):
        record = json.loads(message.value)
        print(record) # noqa


def start(*, instance: KConsumer):
    instance.start()
    while instance.alive:
        for msg in instance:
            instance.process_message(msg)
        sleep(3)
        instance.stop()
    instance.close()
