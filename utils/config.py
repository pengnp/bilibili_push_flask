import os


#  文件路径
PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_YAML_PATH = os.path.join(PATH, 'static/datafile/data.yml')
TEMPLATES_PATH = os.path.join(PATH, 'templates')
NEW_IMG_PATH = os.path.join(PATH, 'static/img/new')
OLD_IMG_PATH = os.path.join(PATH, 'static/img/old')


#  邮箱配置
USER_EMAIN = 'download_reminder@qq.com'
USER_EMAIN_PASSWORD = 'quhnwhuafdefbddg'


# 动作标识
class BILI_EVENT:
    ALL_EVENT = {
        'push': False,
        'update': False,
        'check': False
    }

