import json
import logging
from collections.abc import Callable
from time import sleep
from typing import Any

from kafka import KafkaConsumer, KafkaProducer

from models.message import BrokerMessageModel, UseCase
from models.profile import ProfileMovieReadModel, ProfileReadModel
from use_cases.abstract_publisher import AbstractPublisher

logger = logging.getLogger(__name__)


class KProducer(AbstractPublisher):
    def __init__(self, *, config: dict, topic: str):
        host = config.get('host')
        port = config.get('port')
        self.kafka_producer = KafkaProducer(bootstrap_servers=[f'{host}:{port}'])
        self.topic = topic

    def send(self, *, message: BrokerMessageModel):
        logger.debug('Preparing to send message')
        value_model = None
        key = ''
        match message.use_case:
            case UseCase.profile_change.value:
                value_model = ProfileReadModel(**message.payload)
                key = str(value_model.id)
            case UseCase.profile_movie_change.value:
                value_model = ProfileMovieReadModel(**message.payload)
                key = str(value_model.profile_id)
        self._on_send(model=BrokerMessageModel(use_case=message.use_case, payload=value_model.dict()), key=key) # noqa
        logger.info('Message sent successfully')

    def _on_send(self, *, key: str, model: BrokerMessageModel):
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
        logger.info('Starting KConsumer')
        self._running = True

    def stop(self):
        logger.info('Stopping KConsumer')
        self._running = False

    @staticmethod
    def _default_handler(message: Any):
        record = json.loads(message.value)
        print(record) # noqa
        logger.info('Record processed: %s', record)


def start(*, instance: KConsumer):
    logger.debug('Starting consumer instance')
    instance.start()
    while instance.alive:
        for msg in instance:
            instance.process_message(msg)
        sleep(3)
        instance.stop()
    instance.close()
    logger.info('Consumer instance stopped')
