import asyncio
import json

from dependency_injector.wiring import Provide, inject

from core.containers import Container
from core.settings import settings
from endpoints.consumers.models import KafkaMessageModel
from infrastructure.kafka_broker import KConsumer
from models.profile import ProfileMovieUpdateModel
from use_cases.profile_service import ProfileService


@inject
def handle_favorite_movies_message(
    message: KafkaMessageModel,
    profile_service: ProfileService = Provide[Container.profile_service],
):
    try:
        payload = json.loads(message.value)
        asyncio.run(
            profile_service.movie_update(
                profile_movie_update_model=ProfileMovieUpdateModel(**json.loads(payload)),
            ),
        )

    except (json.decoder.JSONDecodeError, TypeError, AttributeError):
        pass


def get_on_favorite_movies_change_consumer(
    *,
    bootstrap_servers: list[str],
    auto_offset_reset: str,
    group_id: str,
) -> KConsumer:
    return KConsumer(
        'user-content',
        process_message=handle_favorite_movies_message,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset=auto_offset_reset,
        group_id=group_id,
    )
