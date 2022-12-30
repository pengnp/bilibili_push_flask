from flask import Blueprint, render_template, request, session, redirect, url_for
from utils.yaml_util import YamlUtil
from utils.config import DATA_YAML_PATH, BILI_EVENT, IMG_PATH
from utils.bilibili import BILIBILI
from utils.get_calendar import get_data
import datetime
import os
import json
from utils.decorator import is_login, is_admin, thread_check

BILI = BILIBILI()
yaml_func = YamlUtil(DATA_YAML_PATH)
user_blue = Blueprint('user', __name__, url_prefix='/')


@user_blue.route('/', methods=['POST', 'GET'])
def login():
    img_list = json.dumps({'img': os.listdir(IMG_PATH)}, ensure_ascii=False)
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        user_list = yaml_func.read
        if user_name in user_list:
            session['user_name'] = user_name
            session.permanent = True
            user_list[user_name]['login_time'] = datetime.datetime.now().strftime('%Y-%m-%d')
            yaml_func.write_w(user_list)
            return redirect(url_for('user.follows'))
        else:
            return f'<h1>用户不存在，请联系管理员添加</h1>'
    else:
        return render_template('login.html', data_dict=get_data(), img_list=img_list)


@user_blue.route('/follows', methods=['GET'])
@is_login
def follows():
    user_list = yaml_func.read
    user_name = session.get('user_name')
    follows = user_list[user_name]['mids']
    return render_template('demo_follow.html', follows=follows, user_name=user_name)


@user_blue.route('/users', methods=['GET', 'POST'])
@is_admin
@is_login
def users():
    user_list = yaml_func.read
    user_info = {}
    thread_info = {}
    for k, v in user_list.items():
        user_info[k] = [
            v['email'],
            '是' if v['push'] == 'Y' else '否',
            '是' if v['check'] == 'Y' else '否',
            '是' if v['update'] == 'Y' else '否',
            v['login_time']
        ]
    thread_info['push'] = 'true' if BILI_EVENT.ALL_EVENT['push'] else 'false'
    thread_info['update'] = 'true' if BILI_EVENT.ALL_EVENT['update'] else 'false'
    thread_info['check'] = 'true' if BILI_EVENT.ALL_EVENT['check'] else 'false'
    return render_template('demo_user.html', user_list=user_info, thread_info=thread_info)


@user_blue.route('/add_user', methods=['POST'])
@thread_check
@is_login
def add_user():
    user_name = request.form.get('user_name')
    user_mid = request.form.get('user_id')
    user_email = request.form.get('user_email')
    user_model = request.form.get('user_model')
    if user_name not in yaml_func.read:
        info = {
            user_name: {
                'mid': user_mid,
                'email': user_email,
                'model': user_model,
                'mids': {},
                'update': 'N',
                'check': 'N',
                'push': 'N',
                'login_time': '暂无登录'
            }
        }
        yaml_func.write_a(info)
        BILI.start(user_name, BILI.update_user_info)
        return redirect(url_for('user.users'))
    else:
        return f'<h1>用户已存在</h1>'


@user_blue.route('/del_user', methods=['POST'])
@thread_check
@is_login
def del_user():
    user_name = request.form.get('user_name')
    if user_name != '彭能鹏':
        user_list = yaml_func.read
        del user_list[user_name]
        yaml_func.write_w(user_list)
        return redirect(url_for('user.users'))
    else:
        return f'<h1>你是超级管理员，不能删除自己</h1>'


@user_blue.route('/update_user', methods=['POST'])
@thread_check
@is_login
def update_user():
    user_name = request.form.get('user_name')
    user_email = request.form.get('email')
    push_type = request.form.get('push')
    check_type = request.form.get('check')
    update_type = request.form.get('update')
    if not all([user_email, push_type, check_type, update_type]):
        return render_template('demo_user.html')
    else:
        user_list = yaml_func.read
        user_list[user_name]['email'] = user_email
        user_list[user_name]['push'] = push_type
        user_list[user_name]['check'] = check_type
        user_list[user_name]['update'] = update_type
        yaml_func.write_w(user_list)
        return redirect(url_for('user.users'))


@user_blue.route('/log_out', methods=['GET'])
def log_out():
    try:
        del session['user_name']
    except:
        pass
    return redirect(url_for('user.login'))
