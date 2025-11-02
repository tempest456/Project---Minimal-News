from datetime import datetime

from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from . import db

categories = {
    'nepal': 1,
    'world': 2,
    'business': 4,
    'sports': 8,
    'entertainment': 16,
    'science-technology': 32,
}


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    preferred_time = db.Column(db.String(8), index=True)
    subscriptions = db.Column(db.Integer)
    corona_update = db.Column(db.Boolean, default=False)
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.subscriptions is None:
            self.subscriptions = 0

    def __repr__(self):
        return f'User {self.email}'

    def add_subscription(self, category):
        if not self.is_subscribed(category):
            self.subscriptions += categories[category]

    def remove_subscription(self, category):
        if self.is_subscribed(category):
            self.subscriptions -= categories[category]

    def is_subscribed(self, category):
        return self.subscriptions & categories[category] == categories[category]

    def list_subscriptions(self):
        subscription_list = list()
        for category in categories:
            if self.is_subscribed(category):
                subscription_list.append(category)
        return subscription_list

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    @classmethod
    def confirm(cls, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False

        if not cls.query.filter_by(id=data.get('confirm')):
            return False
        user = cls.query.filter_by(id=data.get('confirm')).first()
        user.confirmed = True
        db.session.add(user)
        return True


class News(db.Model):
    __tablename__='news'
    id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.String(128), unique=True)
    url = db.Column(db.String(256))
    summarized_body = db.Column(db.Text())
    category = db.Column(db.String(16))
    date = db.Column(db.DateTime(), default=datetime.utcnow)
    
    def __repr__(self):
        return f'[{self.date}]: {self.headline}'
    
