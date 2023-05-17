import json

from dependency_injector.wiring import inject, Provide

from core.containers import Container
from models.models import KafkaMessageModel
from infrastructure.kafka_broker import KConsumer
from models.profile import UserFavoriteMoviesModel
from use_cases.profile_service import ProfileService


@inject
def handle_favorite_movies_message(message: KafkaMessageModel, profile_service: ProfileService = Provide[Container.profile_service]):
    try:
        payload = json.loads(message.value)
        profile_service.favorite_movies_update(
            user_favorite_movies_model=UserFavoriteMoviesModel(**json.loads(payload)),
        )
    except json.decoder.JSONDecodeError:
        pass


def get_on_favorite_movies_change_consumer(
    *,
    bootstrap_servers: list[str],
    auto_offset_reset: str,
    group_id: str,
) -> KConsumer:
    return KConsumer(
        'user-favorite-movies',
        process_message=handle_favorite_movies_message,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset=auto_offset_reset,
        group_id=group_id,
    )