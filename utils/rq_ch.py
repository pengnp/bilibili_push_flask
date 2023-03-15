from utils.config import *
from utils.log import logger


def check_cu():
    df = current_minute(orders, fields='close')
    error_info = df[df.close > 100000]
    logger.info(f'\n{error_info}')