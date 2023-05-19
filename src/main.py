from http import HTTPStatus

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import NoResultFound
from starlette.responses import PlainTextResponse

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
    container.wire(modules=['endpoints.api.v1.profiles'])
    container.config.from_pydantic(settings)
    application.container = container
    application.include_router(profiles.router, prefix='/api/v1/profiles', tags=['profiles'])
    return application


app = create_app()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=HTTPStatus.BAD_REQUEST)


@app.exception_handler(NoResultFound)
async def not_found_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=HTTPStatus.NOT_FOUND)
