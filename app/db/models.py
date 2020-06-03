import sqlalchemy.orm
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app import clock

Base = declarative_base()


def insert_me(obj, session: sqlalchemy.orm.Session):
    session.add(obj)
    session.commit()
    return obj


def delete_me(obj, session: sqlalchemy.orm.Session):
    session.delete(obj)
    session.commit()
    return None


Base.insert_me = insert_me
Base.delete_me = delete_me


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    uid = Column(Integer)
    username = Column(String(255))
    full_name = Column(String(30))
    email_address = Column(String(100))
    phone_number = Column(String(20))
    location = Column(String(100))
    limit = Column(Integer, default=100)
    active = Column(Boolean, default=True)
    receive_notifications = Column(Boolean, default=True)
    created = Column(DateTime, default=clock.now())
    edited = Column(DateTime, default=clock.now())

    def __init__(self,
                 uid,
                 username=None,
                 full_name=None,
                 email_address=None,
                 phone_number=None,
                 location=None,
                 limit=100,
                 active=True,
                 receive_notifications=True):
        self.uid = uid
        self.username = username
        self.full_name = full_name
        self.email_address = email_address
        self.phone_number = phone_number
        self.location = location
        self.limit = limit
        self.active = active
        self.receive_notifications = receive_notifications

    def __repr__(self):
        return f"User(id={self.id}, uid={self.uid}, username={self.username}, " \
               f"full_name={self.full_name}, email_address={self.email_address}, " \
               f"phone_number={self.phone_number}, location={self.location}), limit={self.limit}, " \
               f"active={self.active}, receive_notifications={self.receive_notifications}, " \
               f"created={self.created}, edited={self.edited})"


class Card(Base):
    __tablename__ = 'card'

    STATUSES = {
        0: 'created',
        1: 'listed',
        9: 'sold',
    }

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String(100))
    price = Column(Integer, default=False)
    status = Column(Integer)
    created = Column(DateTime, default=clock.now())
    edited = Column(DateTime, default=clock.now())

    owner = relationship('User', backref='owner_cards', foreign_keys=[owner_id])

    def __init__(self,
                 owner_id,
                 name,
                 price):
        self.owner_id = owner_id
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Card(id={self.id}, user_id={self.owner_id}, name={self.name}, price={self.price}, " \
               f"status={self.status}, created={self.created}, edited={self.edited})"


class Subscription(Base):
    __tablename__ = 'subscription'

    TYPES = {
        0: 'card_id',
        1: 'space_add_hundred',
        2: 'space_add_thousand',
        3: 'space_add_5_thousand',
    }

    id = Column(Integer, primary_key=True)
    subscriber_id = Column(Integer, ForeignKey('user.id'))
    type = Column(Integer, default=0)
    card_id = Column(Integer, ForeignKey('card.id'))
    created = Column(DateTime, default=clock.now())

    subscriber = relationship('User', backref='user_subscriptions', foreign_keys=[subscriber_id])
    card = relationship('Card', backref='card_subscriptions', foreign_keys=[card_id])

    def __init__(self,
                 subscriber_id,
                 card_id):
        self.subscriber_id = subscriber_id
        self.card_id = card_id

    def __repr__(self):
        return f"Subscription(id={self.id}, user_id={self.subscriber_id}, " \
               f"card_id={self.card_id}, created={self.created})"


class Demand(Base):
    __tablename__ = 'demand'
    id = Column(Integer, primary_key=True)
    requestor_id = Column(Integer, ForeignKey('user.id'))
    card_name = Column(String(100))
    created = Column(DateTime, default=clock.now())

    requestor = relationship('User', backref='user_demands', foreign_keys=[requestor_id])

    def __init__(self,
                 requestor_id,
                 card_id):
        self.requestor_id = requestor_id
        self.card_name = card_id

    def __repr__(self):
        return f"Demand(id={self.id}, user_id={self.requestor_id}, " \
               f"card_id={self.card_name}, created={self.created})"
