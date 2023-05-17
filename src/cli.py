import click

from core.containers import Container
from core.settings import settings
from endpoints.consumers.on_favorite_movies_change_consumer import get_on_favorite_movies_change_consumer
from infrastructure.kafka_broker import start


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    '--host',
    type=str,
    default=settings.kafka_settings.host,
    show_default=True,
)
@click.option(
    '--port',
    type=int,
    default=settings.kafka_settings.port,
    show_default=True,
)
@click.option(
    '--auto_offset_reset',
    type=str,
    default=settings.kafka_settings.auto_offset_reset,
    show_default=True,
)
@click.option(
    '--group_id',
    type=str,
    default=settings.kafka_settings.group_id,
    show_default=True,
)
def on_favorite_movies_change_consumer(
    host: str,
    port: int,
    auto_offset_reset: str,
    group_id: str,
):
    container = Container()
    container.config.from_pydantic(settings)
    consumer = get_on_favorite_movies_change_consumer(
        bootstrap_servers=[f'{host}:{port}'],
        auto_offset_reset=auto_offset_reset,
        group_id=group_id,
    )
    start(instance=consumer)


if __name__ == '__main__':
    cli()