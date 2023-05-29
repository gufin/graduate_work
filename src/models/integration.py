from enum import Enum


class AuthServiceOperation(str, Enum):
    check_user = 'check-user'
    check_group = 'check-group'
