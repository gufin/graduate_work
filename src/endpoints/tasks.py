from celery.signals import worker_process_init
from dependency_injector.wiring import Provide, inject

from core.containers import Container
from core.settings import settings
from infrastructure.celery_worker import app
from models.message import BrokerMessageModel
from use_cases.abstract_publisher import AbstractPublisher


@worker_process_init.connect
def init(sender, **kwargs):
    container = Container()
    container.wire(modules=[__name__])
    container.config.from_pydantic(settings)


@app.task
@inject
def send_message_task(
    *,
    use_case: str,
    payload: dict,
    publisher: AbstractPublisher = Provide[Container.publisher],
):
    publisher.send(message=BrokerMessageModel(use_case=use_case, payload=payload))
