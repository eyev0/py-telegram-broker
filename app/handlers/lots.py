from contextlib import suppress
from typing import List

from aiogram import types
from aiogram.dispatcher.filters.state import default_state
from aiogram.dispatcher.handler import SkipHandler
from aiogram.utils.exceptions import MessageCantBeDeleted
from loguru import logger
from sqlalchemy import join

from app.middlewares.i18n import i18n
from app.misc import dp
from app.models.db import db
from app.models.item import Item
from app.models.lot import Lot
from app.models.user import User
from app.utils.states import States

_ = i18n.gettext


@dp.message_handler(commands=["mylots"], state=default_state)
async def mylots(message: types.Message, user: User):
    logger.info("User {user} requested his lots", user=user.id)
    with suppress(MessageCantBeDeleted):
        await message.delete()

    user_lots = (
        await db.select([Item.name, Lot.id, Lot.price])
        .select_from(join(Lot, Item))
        .where(Lot.user_id == user.id)
        .gino.all()
    )
    text = [
        _("List of your lots:"),
        *[
            _("lot_id={id}, {name}, price: {price}").format(
                id=lot_item.id, name=lot_item.name, price=lot_item.price
            )
            for lot_item in user_lots
        ],
    ]
    await message.answer("\n".join(text))


def _validate_upload(raw_text: str,) -> int:
    n_rows = -1
    raw_text = raw_text.replace("\r", "")
    rows = raw_text.split("\n")
    for a in [row.split(",") for row in rows]:
        if len(a) != 2:
            break
    else:
        n_rows = len(rows)
    return n_rows


def _parse_upload(raw_text: str,) -> List[List[str]]:
    raw_text = raw_text.replace("\r", "")
    rows = raw_text.split("\n")
    result = [x.split(",") for x in rows]
    return result


@dp.message_handler(commands=["upload"], state=default_state)
async def cmd_upload(message: types.Message):
    logger.info("User {user} wants to upload lots", user=message.from_user.id)
    await message.answer(
        _(
            "Скинь мне список карт, которые хочешь загрузить. "
            "Каждая строка должна иметь формат 'Название','Цена'\n"
            "Например, так:\n\n"
            "Серый выхухоль,10\n"
            "Черная вдова,25\n"
            "Скрытный оползень,100\n"
            "..."
        )
    )
    await States.UPLOAD.set()


@dp.message_handler(state=States.UPLOAD)
async def upload_parse_rows(message: types.Message, user: User):
    logger.info("User {user} uploads lots", user=user.id)
    upload_rowcount = _validate_upload(message.text)
    if upload_rowcount < 0:
        await message.answer(
            _(
                "Что-то не так с форматом твоего списка.. "
                "Не могу распарсить твой запрос на добавление. "
                "Приведи все к формату выше."
            )
        )
        raise SkipHandler
    user_lots = (
        await db.select([Item.name, Lot.id, Lot.price])
        .select_from(join(Lot, Item))
        .where(Lot.user_id == user.id)
        .gino.all()
    )
    if upload_rowcount + len(user_lots) > user.lot_limit:
        await message.answer(
            _(
                "Твой лимит объявлений({limit}) превышен! "
                "Нельзя загрузить {num} лотов"
            ).format(limit=user.lot_limit, num=upload_rowcount)
        )
        await default_state.set()
        raise SkipHandler
    for name, price in _parse_upload(message.text):
        item = await Item.create(name=name)
        lot = await Lot.create(user_id=user.id, item_id=item.id, price=int(price))
        logger.info("Item = {item!r}, Lot = {lot!r} - created!", item=item, lot=lot)
    await message.answer(_("Успех!"))
    await default_state.set()


@dp.message_handler(commands=["delete"], state=default_state)
async def cmd_delete(message: types.Message, user: User):
    logger.info("User {user} deletes his lots", user=user.id)
    user_lots = await Lot.load(item=Item).gino.all()
    text = [
        _("Records:"),
        *[
            _("lot_id={id}, {name}, price: {price}").format(
                id=lot.id, name=lot.item.name, price=lot.price
            )
            for lot in user_lots
        ],
        _("deleted!"),
    ]
    await message.answer("\n".join(text))
    for lot in user_lots:
        await lot.delete()
        logger.info("Lot {lot!r} deleted!", lot=lot)
