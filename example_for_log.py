import logging
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_DIR = os.path.join(BASE_DIR, 'main.log')

logger = logging.getLogger(__name__)

def loggin():
    logging.basicConfig(
        level=logging.DEBUG,
        format=(
            '%(asctime)s::[%(levelname)s]::%(message)s, %(name)s, %(lineno)s, %(filename)s'),
        filename=MAIN_DIR,
        handlers=[logging.StreamHandler(sys.stdout)],
        filemode='w'
    )

