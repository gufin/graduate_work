from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.containers import Container
from core.settings import settings
from endpoints.api.v1 import profiles


def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.project_name,
        docs_url='/api/openapi',
        openapi_url='/api/openapi.json',
        default_response_class=ORJSONResponse,
    )
    container = Container()
    container.wire(modules=['endpoints'])
    container.config.from_pydantic(settings)
    application.container = container
    application.include_router(profiles.router, prefix='/api/v1/profiles', tags=['profiles'])
    return application


app = create_app()