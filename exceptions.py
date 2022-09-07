class NotSentException(Exception):
    """Исключения которые не отправляются в телеграмм."""


class CustomTelegramError(NotSentException):
    """Исключения сгенерированные библиотекой telegram."""


class HomeworkListIsEmpty(NotSentException):
    """Список домашних работ пуст."""


class TheServerDidNotSendTheTimeCutoff(NotSentException):
    """Сервер не отправил отсечку по времени."""


class CustomRequestException(Exception):
    """Неверный запрос к серверу."""


class CustomJSONDecodeError(Exception):
    """Некорректный ответ от сервера."""


class HomeworkIsNotList(Exception):
    """Список домашних работ не является списком."""


class CustomNoSuchStatus(Exception):
    """Не найден статус проверки дз."""
