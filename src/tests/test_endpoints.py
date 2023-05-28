import json
from unittest import mock
from uuid import uuid4

from endpoints.consumers.models import KafkaMessageModel
from endpoints.consumers.on_favorite_movies_change_consumer import handle_favorite_movies_message
from endpoints.tasks import send_message_task
from models.message import BrokerMessageModel
from models.profile import ProfileMovieUpdateModel


def test_handle_message__call_properly(container):
    container.wire(modules=['endpoints.consumers.on_favorite_movies_change_consumer'])
    profile_service_mock = mock.AsyncMock()

    expected = ProfileMovieUpdateModel(user_id=uuid4(), movie_id=uuid4(), is_deleted=True)
    message = KafkaMessageModel(
        key=b'1',
        value=json.dumps(expected.json()).encode(),
    )

    with container.profile_service.override(profile_service_mock):
        handle_favorite_movies_message(message=message)

    profile_service_mock.movie_update.assert_called_with(profile_movie_update_model=expected)


def test_send_message_task__call_properly(container):
    container.wire(modules=['endpoints.tasks'])
    publisher_mock = mock.Mock()
    message = BrokerMessageModel(use_case='USE_CASE', payload={'1': 2})

    with container.publisher.override(publisher_mock):
        send_message_task(use_case=message.use_case, payload=message.payload)

    publisher_mock.send.assert_called_with(message=message)
