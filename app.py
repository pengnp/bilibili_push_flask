from flask import Flask
from datetime import timedelta
from blueview.Interface import user_blue
from utils.scheduled_tasks import Config
from flask_apscheduler import APScheduler

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(user_blue)
app.secret_key = 'u2jksidjflsduwerjl'
app.permanent_session_lifetime = timedelta(days=1)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)


#  https://www.cnblogs.com/shenh/p/13366583.html 定时器
#  https://blog.csdn.net/m0_49475727/article/details/115124956 解决定时器问题
