from utils.bilibili import PushAndUpdate


class Config:

    JOBS = [
        {  # 每天01：15执行
            'id': 'job1',
            'func': PushAndUpdate().start,
            'args': ('update',),
            'trigger': 'cron',
            'day_of_week': '0-6',
            'hour': 1,
            'minute': 15,
        },
        {  # 每周日 23:59:00 执行
            'id': 'job2',
            'func': PushAndUpdate().start,
            'args': ('check',),
            'trigger': 'cron',
            'day_of_week': 6,
            'hour': 23,
            'minute': 59
        },
        {  # 每半小时执行
            'id': 'job3',
            'func': PushAndUpdate().start,
            'args': ('push',),
            'trigger': 'interval',
            'minutes': 30
        }
    ]
    # 配置时区
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'
    # 调度器开关
    SCHEDULER_API_ENABLED = True

