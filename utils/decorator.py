from functools import wraps
from flask import session, redirect, url_for, render_template
from utils.config import BILI_EVENT


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
