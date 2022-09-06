import logging
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_DIR = os.path.join(BASE_DIR, 'main.log')


def set_loggin():
    logging.basicConfig(
        level=logging.DEBUG,
        format=(
            '%(asctime)s [%(levelname)s] %(message)s,: '
            '%(name)s, %(lineno)s, %(filename)s'
        ),
        handlers=[logging.StreamHandler(sys.stdout),
                  logging.FileHandler(MAIN_DIR)],
    )
