from app.models.db import BaseModel, TimedBaseModel, db


class Item(TimedBaseModel):
    __tablename__ = "items"

    id = db.Column(
        db.Integer, autoincrement=True, primary_key=True, index=True, unique=True
    )
    name = db.Column(db.String)


class ItemRelatedModel(BaseModel):
    __abstract__ = True

    item_id = db.Column(
        db.ForeignKey(
            f"{Item.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"
        ),
        nullable=False,
    )
