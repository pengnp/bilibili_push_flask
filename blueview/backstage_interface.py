from flask import Blueprint, render_template, request, session, redirect, url_for
from utils.config import IMG_PATH
from utils.tinypng import compress_core
import os
import threading
from utils.decorator import is_admin, is_login

backstage_blue = Blueprint('backstage', __name__, url_prefix='/')


@backstage_blue.route('/upload', methods=['GET', 'POST'])
@is_admin
@is_login
def upload_img():
    if session.get('user_name') == '彭能鹏':
        img_list = os.listdir(IMG_PATH)
        if request.method == 'GET':
            return render_template('backstage.html', img_list=img_list, msg=None)
        else:
            img_date = request.files['img']
            if img_date:
                img_name = img_date.filename
                file_path = os.path.join(IMG_PATH, img_name)
                img_date.save(file_path)
                th = threading.Thread(target=compress_core, args=(file_path, file_path))
                th.daemon = True
                th.start()
                return render_template('backstage.html', img_list=img_list, msg='上传成功')
            else:
                return render_template('backstage.html', img_list=img_list, msg='请选择图片')
    else:
        return render_template('no_permission.html')


@backstage_blue.route('/del_img', methods=['POST'])
def del_img():
    img_name = request.form.get('img_name')
    img_path = os.path.join(IMG_PATH, img_name)
    os.remove(img_path)
    return redirect(url_for('backstage.upload_img'))

