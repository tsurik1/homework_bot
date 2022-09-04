class NotSentException(Exception):
    """Исключения которые не отправляются в телеграмм."""
    pass


class CustomTelegramError(NotSentException):
    """Исключения сгенерированные библиотекой telegram."""
    pass


class WrongAPIResponseCodeError(NotSentException):
    """Ответ сервера не является успешным."""
    pass


class TheServerDidNotSendTheTimeCutoff(NotSentException):
    """Сервер не отправил отсечку по времени."""
    pass


class CustomRequestException(Exception):
    """Неверный запрос к серверу."""
    pass


class CustomJSONDecodeError(Exception):
    """Некорректный ответ от сервера."""
    pass


class HomeworkIsNotList(Exception):
    """Список домашних работ не является списком."""
    pass


class ListIsNotEmpty(Exception):
    """Список домашних работ пуст."""
    pass
