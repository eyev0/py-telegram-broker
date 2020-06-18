from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app.database.mixin import ObjectsListMixin
from app.utils.utils import clock

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    username = Column(String(255))
    first_name = Column(String(100))
    last_name = Column(String(100))
    locale = Column(String(2))
    email_address = Column(String(100))
    phone_number = Column(String(20))
    location = Column(String(100))
    limit = Column(Integer, default=100)
    active = Column(Boolean, default=True)
    receive_notifications = Column(Boolean, default=True)
    created = Column(DateTime, default=clock.now)
    edited = Column(DateTime, default=clock.now)

    def __init__(
        self,
        chat_id,
        username=None,
        first_name=None,
        last_name=None,
        locale=None,
        email_address=None,
        phone_number=None,
        location=None,
        limit=100,
        active=True,
        receive_notifications=True,
    ):
        self.chat_id = chat_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.locale = locale
        self.email_address = email_address
        self.phone_number = phone_number
        self.location = location
        self.limit = limit
        self.active = active
        self.receive_notifications = receive_notifications

    def __repr__(self):
        return (
            f"User(id={self.id}, "
            f"chat_id={self.chat_id}, "
            f"username={self.username}, "
            f"first_name={self.first_name}, "
            f"last_name={self.last_name}, "
            f"locale={self.locale}, "
            f"email_address={self.email_address}, "
            f"phone_number={self.phone_number}, "
            f"location={self.location}, "
            f"limit={self.limit}, "
            f"active={self.active}, "
            f"receive_notifications={self.receive_notifications}, "
            f"created={self.created}, "
            f"edited={self.edited})"
        )


class Item(Base, ObjectsListMixin):
    __tablename__ = "item"

    STATUSES = {
        0: "created",
        1: "listed",
        9: "sold",
    }

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    name = Column(String(100))
    price = Column(Integer, default=False)
    status = Column(Integer, default=0)
    created = Column(DateTime, default=clock.now)
    edited = Column(DateTime, default=clock.now)

    owner = relationship("User", backref="owner_items", foreign_keys=[owner_id])

    def __init__(self, owner_id, name, price):
        self.owner_id = owner_id
        self.name = name
        self.price = price

    def __repr__(self):
        return (
            f"Item(id={self.id}, "
            f"user_id={self.owner_id}, "
            f"name={self.name}, "
            f"price={self.price}, "
            f"status={self.status}, "
            f"created={self.created}, "
            f"edited={self.edited})"
        )

    # ListReprMixin
    _list_mixin_header = "Your cards:\n"

    def row_repr(self):
        return f"id={self.id}, {self.name} - {str(self.price)}р."


class Subscription(Base):
    __tablename__ = "subscription"

    TYPES = {
        0: "item",
        1: "space_add_hundred",
        2: "space_add_thousand",
        3: "space_add_fivethousand",
    }

    id = Column(Integer, primary_key=True)
    subscriber_id = Column(Integer, ForeignKey("user.id"))
    type = Column(Integer, default=0)
    item_id = Column(Integer, ForeignKey("item.id"))
    created = Column(DateTime, default=clock.now)

    subscriber = relationship(
        "User", backref="user_subscriptions", foreign_keys=[subscriber_id]
    )
    item = relationship("Item", backref="item_subscriptions", foreign_keys=[item_id])

    def __init__(self, subscriber_id, card_id):
        self.subscriber_id = subscriber_id
        self.card_id = card_id

    def __repr__(self):
        return (
            f"Subscription(id={self.id}, "
            f"user_id={self.subscriber_id}, "
            f"item_id={self.item_id}, "
            f"created={self.created})"
        )


class Demand(Base):
    __tablename__ = "demand"
    id = Column(Integer, primary_key=True)
    requestor_id = Column(Integer, ForeignKey("user.id"))
    item_name = Column(String(100))
    created = Column(DateTime, default=clock.now)

    requestor = relationship(
        "User", backref="user_demands", foreign_keys=[requestor_id]
    )

    def __init__(self, requestor_id, item_name):
        self.requestor_id = requestor_id
        self.item_name = item_name

    def __repr__(self):
        return (
            f"Demand(id={self.id}, "
            f"user_id={self.requestor_id}, "
            f"item_name={self.item_name}, "
            f"created={self.created})"
        )
