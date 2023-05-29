import logging
from http import HTTPStatus

import aiohttp
from fastapi import Request

from models.integration import AuthServiceOperation
from use_cases.abstract_repositories import AbstractAuthRepository


class AuthClient(AbstractAuthRepository): # noqa WPS338
    def __init__(self, *, base_url: str, schema: dict):
        self.base_url = base_url
        self.schema = schema
        self.logger = logging.getLogger(__name__)

    @property
    def base_api_path(self):
        return self.schema.get('basePath')

    def endpoint(self, *, operation: AuthServiceOperation, method: str) -> tuple[str, dict]:
        paths = [
            (key, item_value)
            for key, item_value in self.schema.get('paths').items()
            if self._check_ref(schema=item_value.get(method), operation=operation)
        ]
        return paths[0] if paths else None

    def _check_ref(self, *, schema: dict, operation: AuthServiceOperation) -> bool: # noqa
        checking_result = False
        if schema:
            for key, item_value in schema.items():
                if isinstance(item_value, dict):
                    checking_result = self._check_ref(schema=item_value, operation=operation)
                else:
                    checking_result = item_value == operation.value and key == 'operationId'
                if checking_result:
                    break
        return checking_result

    async def verify(
        self,
        *,
        operation: AuthServiceOperation,
        token: str,
        roles: str,
        request: Request,
        headers: dict,
    ) -> bool:
        self.logger.debug('Starting verification process')
        session = aiohttp.ClientSession()
        try:
            endpoint = self.endpoint(operation=operation.value, method='get')
            endpoint_name = endpoint[1].get('parameters')[0].get('name')
            calculated_path = ''
            match operation:
                case AuthServiceOperation.check_user:
                    calculated_path = endpoint[0].replace('{' + endpoint_name + '}', roles) # noqa WPS336
                case AuthServiceOperation.check_group:
                    calculated_path = endpoint[0].replace('{' + endpoint_name + '}', request.path_params.get('user_id'))  # noqa WPS336
                    calculated_path += f'?owner_id={request.path_params.get("owner_id")}' # noqa
            url = f'{self.base_url}{self.base_api_path}{calculated_path}'

            async with session.get(
                url,
                headers={'Authorization': f'Bearer {token}'} | headers,
            ) as response:
                await session.close()
                return response.status == HTTPStatus.OK
        except TypeError:
            self.logger.error('Error during verification process')
            return False


class AuthClientMock(AbstractAuthRepository):
    async def verify(
        self,
        *,
        operation: AuthServiceOperation,
        token: str,
        roles: str,
        request: Request,
        headers: dict,
    ) -> bool:
        return True
