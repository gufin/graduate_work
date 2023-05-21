import json
from http import HTTPStatus

import aiofiles
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import NoResultFound
from starlette.responses import PlainTextResponse

from core.containers import Container
from core.settings import settings
from endpoints.api.v1 import profiles
from infrastructure.auth import AuthClient, AuthClientMock
from use_cases import abstract_repositories


def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.project_name,
        docs_url='/api/openapi',
        openapi_url='/api/openapi.json',
        default_response_class=ORJSONResponse,
    )
    container = Container()
    container.wire(modules=['endpoints.api.v1.profiles'])
    container.config.from_pydantic(settings)
    application.container = container
    application.include_router(profiles.router, prefix='/api/v1/profiles', tags=['profiles'])
    return application


app = create_app()


@app.on_event('startup')
async def startup():
    if settings.integration_off:
        abstract_repositories.auth_client = AuthClientMock()
        return
    async with aiofiles.open(settings.auth_api_schema_path, 'r') as schema_file:
        schema_file_data = await schema_file.read()

        abstract_repositories.auth_client = AuthClient(
            base_url=settings.auth_service_url,
            schema=json.loads(schema_file_data),
        )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=HTTPStatus.BAD_REQUEST)


@app.exception_handler(NoResultFound)
async def not_found_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=HTTPStatus.NOT_FOUND)
