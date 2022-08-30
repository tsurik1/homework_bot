import logging
import os
import time

import requests
import telegram

from dotenv import load_dotenv
from telegram.ext import Updater

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_HOME_TOKEN')
TELEGRAM_TOKEN = os.getenv('TOKEN')
TELEGRAM_CHAT_ID = os.getenv('CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def send_message(bot, message):
    """Отправляем сообщение в телеграм."""
    chat_id = TELEGRAM_CHAT_ID
    bot.send_message(chat_id, message)


def get_api_answer(current_timestamp):
    """Делаем запрос."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    if response.status_code != 200:
        raise Exception
    return response.json()


def check_response(response):
    """Проверяем ответ."""
    if not isinstance(response, dict):
        logging.error('ответ не является словарем')
    elif 'homeworks' not in response:
        raise Exception
    elif not isinstance(response['homeworks'], list):
        raise Exception
    elif len(response['homeworks']) == 0:
        raise Exception
    return response['homeworks']


def parse_status(homework):
    """Возвращаем вердикт из словаря статусов."""
    try:
        homework_name = homework['homework_name']
        homework_status = homework['status']
        verdict = HOMEWORK_STATUSES[homework_status]
        return f'Изменился статус проверки работы "{homework_name}". {verdict}'
    except TypeError as error:
        logging.error(f'Возникла ошибка {error} при запросе.')


def check_tokens():
    """Проверка токенов."""
    if PRACTICUM_TOKEN and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        return True
    else:
        return False


def main():
    """Основная логика работы бота."""
    updater = Updater(token=TELEGRAM_TOKEN)

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = 1
    updater.start_polling(poll_interval=RETRY_TIME)
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homework = check_response(response)
            message = parse_status(homework[0])
            send_message(bot, message)
            time.sleep(RETRY_TIME)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            chat_id = TELEGRAM_CHAT_ID
            bot.send_message(chat_id, text=message)
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
