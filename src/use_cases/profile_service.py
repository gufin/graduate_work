import logging

from models.message import UseCase
from models.profile import ProfileCreateModel, ProfileMovieUpdateModel, ProfileReadModel, ProfileUpdateModel
from models.task import JobType
from use_cases.abstract_repositories import AbstractProfileRepository
from use_cases.abstract_worker import AbstractWorker


class ProfileService:
    def __init__(
        self,
        *,
        repository: AbstractProfileRepository,
        worker: AbstractWorker,
    ):
        self.repository = repository
        self.worker = worker
        self.logger = logging.getLogger(__name__)

    async def create(self, *, user_id: str, profile_model: ProfileCreateModel) -> ProfileReadModel:
        self.logger.info('Creating profile for user_id: %s', user_id)
        create_result = await self.repository.create(user_id=user_id, create_model=profile_model)
        self._send_message(use_case=UseCase.profile_change, payload=create_result.dict())
        return create_result

    async def get(self, *, user_id: str) -> ProfileReadModel:
        self.logger.info('Getting profile for user_id: %s', user_id)
        read_result = await self.repository.read(user_id=user_id)
        self._send_message(use_case=UseCase.profile_change, payload=read_result.dict())
        return read_result

    async def update(self, *, user_id: str, update_model: ProfileUpdateModel) -> ProfileReadModel:
        self.logger.info('Updating profile for user_id: %s', user_id)
        update_result = await self.repository.update(user_id=user_id, update_model=update_model)
        self._send_message(use_case=UseCase.profile_change, payload=update_result.dict())
        return update_result

    async def deactivate(self, *, user_id: str) -> ProfileReadModel:
        self.logger.info('Deactivating profile for user_id: %s', user_id)
        deactivate_result = await self.repository.update(
            user_id=user_id,
            update_model=ProfileUpdateModel(is_active=False),
        )
        self._send_message(use_case=UseCase.profile_change, payload=deactivate_result.dict())
        return deactivate_result

    async def movie_update(
        self,
        *,
        profile_movie_update_model: ProfileMovieUpdateModel,
    ):
        self.logger.info('Updating movie in profile')
        update_result = await self.repository.movie_update(update_model=profile_movie_update_model)
        self._send_message(use_case=UseCase.profile_movie_change, payload=update_result.dict())

    async def get_favorite_movie_ids(self, *, user_id: str) -> list:
        self.logger.info('Getting favorite movie IDs for user_id: %s', user_id)
        return await self.repository.get_favorite_movie_ids(user_id=user_id)

    def _send_message(self, *, use_case: UseCase, payload: dict):
        self.logger.info('Sending message for use_case: %s', use_case)
        self.worker.start_job(
            job_type=JobType.SEND_MESSAGE_TASK,
            use_case=use_case.value,
            payload=payload,
        )
