from http import HTTPStatus

from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from use_cases.abstract_repositories import get_auth_client


class JWTBearer(HTTPBearer):
    def __init__(
        self,
        *,
        operation_id: str = 'check-user',
        user_granted_roles: str = 'user',
        auto_error: bool = True,
    ):
        super().__init__(auto_error=auto_error)
        self.operation_id = operation_id
        self.user_granted_roles = user_granted_roles

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if credentials.scheme != 'Bearer':
                raise HTTPException(
                    status_code=HTTPStatus.FORBIDDEN,
                    detail='Invalid authentication scheme.',
                )
            is_valid = await get_auth_client().verify(
                operation_id=self.operation_id,
                token=credentials.credentials,
                roles=self.user_granted_roles,
                request=request,
                headers={'X-Request-Id': request.headers.get('x-request-id')},
            )
            if not is_valid:
                raise HTTPException(
                    status_code=HTTPStatus.FORBIDDEN,
                    detail='access denied',
                )
            return credentials.credentials
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail='Invalid authorization code.',
        )


jwt_auth = JWTBearer()
