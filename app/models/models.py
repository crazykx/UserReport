from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_login import LoginManager, UserMixin

from .base import Base, db

login_manager = LoginManager()


class Seller(Base, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    realname = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    nickname = db.Column(db.String(50), nullable=False, unique=True)
    _password = db.Column('password', db.String(128))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)


class Admin(Base):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    realname = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    nickname = db.Column(db.String(50), nullable=False, unique=True)
    _password = db.Column('password', db.String(128))
    is_super = db.Column(db.SmallInteger, default=0)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'))

    seller = db.relationship('Seller', backref='admin')

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)


class Guest(Base):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    realname = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    company = db.Column(db.String(50))


class Orders(Base):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'))
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'))
    sales = db.Column(db.Float, nullable=False)
    create_date = db.Column(db.Date, default=datetime.now().date)

    seller = db.relationship('Seller', backref='order')
    guest = db.relationship('Guest', backref='order')

    def __repr__(self):
        return '<order {}> seller_id={} guest_id={} sales={} create_date={}'.format(self.id, self.seller_id, self.guest_id, self.sales, self.create_date)


@login_manager.user_loader
def load_user(id):
        seller = Seller.query.filter_by(id=id).first()
        return seller
