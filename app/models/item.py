import enum

import sqlalchemy as sa

from app.models.db import BaseModel, TimedBaseModel, db


class Item(TimedBaseModel):
    __tablename__ = "items"

    id = db.Column(
        db.Integer, autoincrement=True, primary_key=True, index=True, unique=True
    )
    product_id = db.Column(db.Integer, index=True)
    source = db.Column(db.String)
    original_name = db.Column(db.String, index=True)
    set_name = db.Column(db.String, index=True)
    card_type = db.Column(db.String)
    rarity = db.Column(db.String)
    finish = db.Column(db.String)


class ItemRelatedModel(BaseModel):
    __abstract__ = True

    item_id = db.Column(
        db.ForeignKey(
            f"{Item.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"
        ),
        nullable=False,
    )


class LocalizedItem(TimedBaseModel, ItemRelatedModel):
    __tablename__ = "localized_items"

    id = db.Column(
        db.Integer, autoincrement=True, primary_key=True, index=True, unique=True
    )
    language = db.Column(db.String)
    item_name = db.Column(db.String, index=True)
    source_url = db.Column(db.String)
    image_url = db.Column(db.String)


class LocalizedItemRelatedModel(BaseModel):
    __abstract__ = True

    localized_item_id = db.Column(
        db.ForeignKey(
            f"{LocalizedItem.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"
        ),
        nullable=False,
    )


class ItemCondition(enum.Enum):
    near_mint = "Near Mint"
    played = "Played"
    heavily_played = "Heavily Played"


class ItemOption(TimedBaseModel, ItemRelatedModel):
    __tablename__ = "item_options"

    id = db.Column(
        db.Integer, autoincrement=True, primary_key=True, index=True, unique=True
    )
    price = db.Column(db.Float)
    calculated_price = db.Column(db.Float)
    condition = db.Column(sa.Enum(ItemCondition))


class ItemOptionRelatedModel(BaseModel):
    __abstract__ = True

    item_option_id = db.Column(
        db.ForeignKey(
            f"{ItemOption.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"
        ),
        nullable=False,
    )
