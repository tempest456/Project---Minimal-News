from datetime import date
from threading import Thread

from flask import current_app, render_template
from flask_mail import Message

from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(f"{app.config['MAIL_SUBJECT_PREFIX']} {subject}",
                  sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.html= render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def distribute_news(users, template, **kwargs):
    app = current_app._get_current_object()
    with mail.connect() as conn:
        for user in users:
            print(f'Sending email to {user.email}....')
            subject = f'Minimal News for {date.today()}'
            msg = Message(subject=subject, sender=app.config['MAIL_SENDER'],
                          recipients=[user.email])
            msg.html = render_template(template + '.html', user=user, **kwargs)

            conn.send(msg)
