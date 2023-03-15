import os
from rqdatac import *
init()


df = all_instruments('Future')
order_book_ids = df.order_book_id.tolist()
orders = []
for order in order_book_ids:
    if order[-2:] == '99' or order[:2] == 'AG' or order[:2] == 'FG':
        trading_hours = instruments(order).trading_hours
        if '21:01-23:00' in trading_hours or '21:01-01:00' in trading_hours:
            orders.append(order)

#  文件路径
PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_YAML_PATH = os.path.join(PATH, 'static/datafile/data.yml')
TEMPLATES_PATH = os.path.join(PATH, 'templates')
IMG_PATH = os.path.join(PATH, 'static/img/lunbo/')


#  邮箱配置
USER_EMAIN = 'download_reminder@qq.com'
USER_EMAIN_PASSWORD = 'ztdzxbefwbasbcdh'


# 动作标识
class BILI_EVENT:
    ALL_EVENT = {
        'push': False,
        'update': False,
        'check': False
    }


header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63",
    "referer": "https://www.bilibili.com/",
}

