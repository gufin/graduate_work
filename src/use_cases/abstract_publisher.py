from abc import ABC, abstractmethod

from models.message import BrokerMessageModel


class AbstractPublisher(ABC):
    @abstractmethod
    def send(self, *, message: BrokerMessageModel):
        pass
