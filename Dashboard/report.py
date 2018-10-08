# from Map.map_api import *
#
# dengue = get_dengue_clusters()
# for i in dengue:
#     print(i)
#
# psi = get_psi()
# for i in psi:
#     print(i)
#
# weather = get_weather()
# for key, value in weather.items():
#     print(key, value)
from flask_mail import Message
from app import mail, app
from utils import async

@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_report():
    msg = Message(subject="Hello",
                  sender=app.config["MAIL_USERNAME"],
                  recipients=["yue0068@gmail.com"],  # replace with your email for testing
                  body="This is a test email I sent with Gmail and Python!")
    send_async_email(app, msg)
    print('Sent success')

