import os


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
    "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36 Edg/107.0.0.0"
}

