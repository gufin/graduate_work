from http import HTTPStatus

import aiohttp

from use_cases.abstract_repositories import AbstractAuthRepository


class AuthClient(AbstractAuthRepository): # noqa WPS338
    def __init__(self, *, base_url: str, schema: dict):
        self.base_url = base_url
        self.schema = schema

    @property
    def base_api_path(self):
        return self.schema.get('basePath')

    def endpoint(self, *, definition: str, method: str) -> tuple[str, dict]:
        paths = [
            (key, item_value)
            for key, item_value in self.schema.get('paths').items()
            if self._check_ref(schema=item_value.get(method), definition=definition)
        ]
        return paths[0] if paths else None

    def _check_ref(self, *, schema: dict, definition: str) -> bool:
        checking_result = False
        if schema:
            for _, item_value in schema.items():
                if isinstance(item_value, dict):
                    checking_result = self._check_ref(schema=item_value, definition=definition)
                else:
                    checking_result = item_value == f'#/definitions/{definition}'
                if checking_result:
                    break
        return checking_result

    async def verify(self, *, token: str, roles: str, headers: dict) -> bool:
        session = aiohttp.ClientSession()
        try:
            endpoint = self.endpoint(definition='User%20Access', method='get')
            endpoint_name = endpoint[1].get('parameters')[0].get('name')
            calculated_path = endpoint[0].replace('{' + endpoint_name + '}', roles) # noqa WPS336
            url = f'{self.base_url}{self.base_api_path}{calculated_path}'

            async with session.get(
                url,
                headers={'Authorization': f'Bearer {token}'} | headers,
            ) as response:
                await session.close()
                return response.status == HTTPStatus.OK
        except TypeError:
            return False

    async def is_profile_in_group(self, *, group_id: str,  user_id: str) -> bool:
        return True


class AuthClientMock(AbstractAuthRepository):
    async def verify(self, *, token: str, roles: str, headers: dict) -> bool:
        return True
