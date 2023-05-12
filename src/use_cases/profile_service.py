from models.profile import ProfileModel


class ProfileService:
    def __init__(self):
        pass

    def create(self):
        """Создать профиль пользователя"""
        pass

    def update(self, *, user_id: str, profile: ProfileModel):
        """Обновить профиль пользователя"""
        pass

    def get(self, user_id: str | None = None) -> ProfileModel | list[ProfileModel]:
        """Получить профиль одного пользователя по индефикатору
        или если индефитор пустой показать всех.
        """
        pass

    def delete(self, user_id: str):
        """Заморозить профиль пользователя"""
        pass
