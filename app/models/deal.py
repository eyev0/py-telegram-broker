import enum

import sqlalchemy as sa

from app.models.db import TimedBaseModel, db
from app.models.lot import LotRelatedModel
from app.models.user import UserRelatedModel


class DealType(enum.Enum):
    lot_tax = "tax"
    lot_space = "space"


class Deal(TimedBaseModel, UserRelatedModel, LotRelatedModel):
    __tablename__ = "deals"

    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    type = db.Column(sa.Enum(DealType), default=DealType.lot_tax)
