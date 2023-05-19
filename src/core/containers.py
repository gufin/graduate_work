from dependency_injector import containers, providers

from infrastructure.celery_worker import CeleryWorker
from infrastructure.kafka_broker import KProducer
from infrastructure.postgres_profile_repository import PostgresProfileRepository
from use_cases.profile_service import ProfileService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    profile_repository = providers.Singleton(PostgresProfileRepository)

    worker = providers.Singleton(CeleryWorker)

    publisher = providers.Singleton(
        KProducer,
        config=config.kafka_settings,
        topic='profile',
    )

    profile_service = providers.Factory(
        ProfileService,
        repository=profile_repository,
        worker=worker,
    )
