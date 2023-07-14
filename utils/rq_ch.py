from utils.config import *
from utils.log import logger
import datetime


def get_future_latest_trading_date_check():
    now_time = datetime.datetime.now().strftime('%Y%m%d%H%M')
    text = get_future_latest_trading_date()
    logger.info(f'当前日期为：{now_time},API返回时间为：{text}\n')