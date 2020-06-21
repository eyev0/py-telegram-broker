import enum

import sqlalchemy as sa
from sqlalchemy.sql import expression

from app.models.db import BaseModel, TimedBaseModel, db
from app.models.item import ItemRelatedModel
from app.models.user import UserRelatedModel


class LotStatus(enum.Enum):
    created = 0
    published = 1
    closed = 9


class Lot(TimedBaseModel, UserRelatedModel, ItemRelatedModel):
    __tablename__ = "lots"

    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    is_demand = db.Column(db.Boolean, default=expression.false())
    price = db.Column(db.Integer, default="0")
    status = db.Column(sa.Enum(LotStatus), default=LotStatus.created)


class LotRelatedModel(BaseModel):
    __abstract__ = True

    lot_id = db.Column(
        db.ForeignKey(
            f"{Lot.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"
        ),
        nullable=False,
    )
