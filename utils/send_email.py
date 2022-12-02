import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from utils.config import USER_EMAIN, USER_EMAIN_PASSWORD


class SendEmail:

    def __init__(self, subject, email, msg):
        self._send = USER_EMAIN
        self._password = USER_EMAIN_PASSWORD
        self._subject = subject
        self._email = email
        self._robot = 'Mr.P'
        self._msg = msg

    def send_email(self):
        msg_root = MIMEMultipart('mixed')
        msg_root['From'] = Header(self._robot, 'utf-8')
        msg_root['To'] = Header(','.join(self._email), 'utf-8')
        msg_root['Subject'] = Header(self._subject, 'utf-8')
        msg_html = MIMEText(self._msg, 'html', 'utf-8')
        msg_root.attach(msg_html)
        s = smtplib.SMTP_SSL('smtp.qq.com')
        s.login(self._send, self._password)
        s.sendmail(self._send, self._email, msg_root.as_string())