class BaseException(Exception):
    detail = 'Неожиданная ошибка'

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BaseException):
    detail = 'Объект не найден'

class AllRoomsAreBookedException(BaseException):
    detail = 'Не осталось свободных номеров'

class EmailAlreadyExistsException(BaseException):
    detail = 'Пользователь с таким email уже существует'