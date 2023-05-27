from http import HTTPStatus

import aiohttp
from fastapi import Request

from use_cases.abstract_repositories import AbstractAuthRepository


class AuthClient(AbstractAuthRepository): # noqa WPS338
    def __init__(self, *, base_url: str, schema: dict):
        self.base_url = base_url
        self.schema = schema

    @property
    def base_api_path(self):
        return self.schema.get('basePath')

    def endpoint(self, *, operation_id: str, method: str) -> tuple[str, dict]:
        paths = [
            (key, item_value)
            for key, item_value in self.schema.get('paths').items()
            if self._check_ref(schema=item_value.get(method), operation_id=operation_id)
        ]
        return paths[0] if paths else None

    def _check_ref(self, *, schema: dict, operation_id: str) -> bool: # noqa
        checking_result = False
        if schema:
            for key, item_value in schema.items():
                if isinstance(item_value, dict):
                    checking_result = self._check_ref(schema=item_value, operation_id=operation_id)
                else:
                    checking_result = item_value == operation_id and key == 'operationId'
                if checking_result:
                    break
        return checking_result

    async def verify(self, *, operation_id: str, token: str, roles: str, request: Request, headers: dict) -> bool:
        session = aiohttp.ClientSession()
        try:
            endpoint = self.endpoint(operation_id=operation_id, method='get')
            endpoint_name = endpoint[1].get('parameters')[0].get('name')
            calculated_path = ''
            match operation_id:
                case 'check-user':
                    calculated_path = endpoint[0].replace('{' + endpoint_name + '}', roles) # noqa WPS336
                case 'check-group':
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
            return False


class AuthClientMock(AbstractAuthRepository):
    async def verify(self, *, operation_id: str, token: str, roles: str, request: Request, headers: dict) -> bool:
        return True
