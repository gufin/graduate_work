from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from models.message import UseCase
from models.profile import ProfileCreateModel, ProfileReadModel
from models.task import JobType


@pytest.mark.asyncio
async def test_create__call_properly(container):
    expected_result = ProfileReadModel(
        id=uuid4(),
        user_id=uuid4(),
        first_name='first_name',
        last_name='last_name',
        patronymic='patronymic',
        phone='phone',
        is_active=True,
    )
    repository_mock = AsyncMock()
    repository_mock.create = AsyncMock(return_value=expected_result)
    worker_mock = Mock()
    profile_model = ProfileCreateModel(
        first_name=expected_result.first_name,
        last_name=expected_result.last_name,
        patronymic=expected_result.patronymic,
        phone=expected_result.phone,
    )

    with container.profile_repository.override(repository_mock):
        with container.worker.override(worker_mock):
            await container.profile_service().create(
                user_id=expected_result.user_id,
                profile_model=profile_model,
            )

    worker_mock.start_job.assert_called_with(
        job_type=JobType.SEND_MESSAGE_TASK,
        use_case=UseCase.profile_change.value,
        payload=expected_result.dict(),
    )
    repository_mock.create.assert_called_with(
        user_id=expected_result.user_id,
        create_model=profile_model,
    )
