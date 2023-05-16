import json
from collections.abc import Callable
from typing import Any

from kafka import KafkaConsumer
from time import sleep


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
        print(record)


def start(*, instance: KConsumer):
    instance.start()
    while instance.alive:
        for msg in instance:
            instance.process_message(msg)
        sleep(3)
        instance.stop()
    instance.close()
