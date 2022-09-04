class NotSentException(Exception):
    """Исключения которые не отправляются в телеграмм."""


class CustomTelegramError(NotSentException):
    """Исключения сгенерированные библиотекой telegram."""


class WrongAPIResponseCodeError(NotSentException):
    """Ответ сервера не является успешным."""


class TheServerDidNotSendTheTimeCutoff(NotSentException):
    """Сервер не отправил отсечку по времени."""


class CustomRequestException(Exception):
    """Неверный запрос к серверу."""


class CustomJSONDecodeError(Exception):
    """Некорректный ответ от сервера."""


class HomeworkIsNotList(Exception):
    """Список домашних работ не является списком."""


class ListIsNotEmpty(Exception):
    """Список домашних работ пуст."""
