from functools import wraps
from flask import session, redirect, url_for, render_template
from utils.config import BILI_EVENT
from time import sleep
import random


def is_login(func):
    @wraps(func)
    def check_login(*args, **kwargs):
        user_name = session.get('user_name')
        if user_name:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('user.login'))
    return check_login


def thread_check(func):
    @wraps(func)
    def check_thread(*args, **kwargs):
        if not BILI_EVENT.ALL_EVENT['update'] and not BILI_EVENT.ALL_EVENT['push'] and not BILI_EVENT.ALL_EVENT['check']:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('user.users'))
    return check_thread


def is_admin(func):
    @wraps(func)
    def check_user(*args, **kwargs):
        user_name = session.get('user_name')
        if user_name == '彭能鹏':
            return func(*args, **kwargs)
        else:
            return render_template('no_permission.html')
    return check_user


def retry(func):
    @wraps(func)
    def retry_fun(*args, **kwargs):
        response = ''
        for _ in range(3):
            sleep(random.uniform(1.0, 3.0))
            response = func(*args, **kwargs)
            if response['code'] == 0:
                return response
            print(f'{args[1]}失败重试, 接口返回：{response}')
        print(f'{args[1]}请求有误, 接口返回：{response}')
        return None
    return retry_fun
