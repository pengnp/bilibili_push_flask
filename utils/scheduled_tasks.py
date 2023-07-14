# from utils.bilibili import BILIBILI
from utils.rq_ch import get_future_latest_trading_date_check


# BILI = BILIBILI()


class Config:

    JOBS = [
        # {  # 每天01：15执行
        #     'id': 'job1',
        #     'func': BILI.start,
        #     'args': ('update', BILI.update_user_info),
        #     'trigger': 'cron',
        #     'day_of_week': '0-6',
        #     'hour': 1,
        #     'minute': 15,
        # },
        # {  # 每周日 23:59:00 执行
        #     'id': 'job2',
        #     'func': BILI.start,
        #     'args': ('check', BILI.week_chenck),
        #     'trigger': 'cron',
        #     'day_of_week': 6,
        #     'hour': 23,
        #     'minute': 45
        # },
        # {  # 每半小时执行
        #     'id': 'job3',
        #     'func': BILI.start,
        #     'args': ('push', BILI.push),
        #     'trigger': 'interval',
        #     'minutes': 30,
        # }

        # {
        #     'id': 'job3',
        #     'func': check_cu,
        #     'trigger': 'interval',
        #     'minutes': 1,
        #     'start_date': '2023-02-14 17:05',
        #     'end_date': '2023-02-14 17:10'
        # },
        {  # 每天20：56执行
            'id': 'job1',
            'func': get_future_latest_trading_date_check,
            'trigger': 'cron',
            'day_of_week': '0-6',
            'hour': 20,
            'minute': 56,
            'misfire_grace_time': 3600
        },
        {  # 每天10：30执行
            'id': 'job2',
            'func': get_future_latest_trading_date_check,
            'trigger': 'cron',
            'day_of_week': '0-6',
            'hour': 16,
            'minute': 52,
            'misfire_grace_time': 3600
        },
    ]
    # 配置时区
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'
    # 调度器开关
    SCHEDULER_API_ENABLED = True

