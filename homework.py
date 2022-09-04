import logging
import os
import time
from http import HTTPStatus
from json import JSONDecodeError

import requests
import telegram
from dotenv import load_dotenv
from requests.exceptions import RequestException
from telegram import TelegramError

from example_for_log import set_loggin
from exceptions import (
    CustomJSONDecodeError,
    CustomRequestException,
    CustomTelegramError,
    HomeworkIsNotList,
    ListIsNotEmpty,
    NotSentException,
    TheServerDidNotSendTheTimeCutoff,
    WrongAPIResponseCodeError
)

load_dotenv()

logger = logging.getLogger(__name__)

PRACTICUM_TOKEN = os.getenv('PRACTICUM_HOME_TOKEN')
TELEGRAM_TOKEN = os.getenv('TOKEN')
TELEGRAM_CHAT_ID = os.getenv('CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_VERDICT = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def send_message(bot: "telegram.bot.Bot", message: str) -> None:
    """Отправляем сообщение в телеграм."""
    logger.info(message)
    try:
        bot.send_message(TELEGRAM_CHAT_ID, text=message)
    except TelegramError as error:
        raise CustomTelegramError('ошибка отправки сообщения') from error


def get_api_answer(current_timestamp: int) -> dict:
    """Делает запрос к единственному эндпоинту API-сервиса."""
    logger.info("Делаем запрос к единственному эндпоинту API-сервиса.")
    params = {'from_date': current_timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    except RequestException as exc:
        raise CustomRequestException(
            'неверный запрос к серверу'
        ) from exc
    if response.status_code != HTTPStatus.OK:
        raise WrongAPIResponseCodeError(
            'Ответ сервера не является успешным:'
            f' request params={params};'
            f' http_code={response.status_code};'
            f' reason={response.reason};'
        )
    try:
        return response.json()
    except JSONDecodeError as exc:
        raise CustomJSONDecodeError('некорректный ответ сервера') from exc


def check_response(response: dict) -> dict:
    """Проверяем ответ API на корректность."""
    logger.info("Проверяем ответ ответ API на корректность.")
    if not isinstance(response, dict):
        raise TypeError(response)
    if 'homeworks' not in response:
        raise KeyError
    list_homework: list = response['homeworks']
    if not isinstance(list_homework, list):
        raise HomeworkIsNotList
    if not list_homework:
        raise ListIsNotEmpty
    if 'current_date' not in response:
        raise TheServerDidNotSendTheTimeCutoff(
            'сервер не отправил отсечку времени'
        )
    return list_homework[0]


def parse_status(homework: dict) -> str:
    """Возвращаем вердикт из словаря статусов."""
    if 'homework_name' not in homework:
        raise KeyError
    homework_name = homework['homework_name']
    homework_status = homework['status']
    logger.info("Возвращаем вердикт из словаря статусов.")
    verdict = HOMEWORK_VERDICT[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens() -> bool:
    """Проверка наличия токенов."""
    logger.info("Проверка наличия токенов.")
    return all((PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID))


def main():
    """Основная логика работы бота."""
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = 0
    current_status = str()
    if not check_tokens():
        logger.critical('отановка программы, отсутствуют токены')
        exit()
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homework = check_response(response)
            message = parse_status(homework)
            current_timestamp = response['current_date']
            if message != current_status:
                current_status = message
                send_message(bot, current_status)
            else:
                logger.INFO('статус не изменился')
        except NotSentException as exc:
            raise NotSentException('какая-то ошибка') from exc
        except Exception as error:
            logger.error(f'Сбой в работе программы: {error}')
            try:
                send_message(bot, message)
            except TelegramError as error:
                logger.error(f'ошибка отправки сообщения{error}')
        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        raise Exception from exc
