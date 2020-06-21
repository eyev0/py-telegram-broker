from aiogram import types
from aiogram.dispatcher.filters.state import default_state
from sqlalchemy import join

from app.middlewares.i18n import i18n
from app.misc import dp
from app.models.item import Item
from app.models.lot import Lot
from app.models.user import User
from app.utils.states import States

_ = i18n.gettext


@dp.message_handler(state=States.SEARCH)
async def search_command(message: types.Message):
    await default_state.set()


@dp.message_handler(commands=["lots"], state=default_state)
async def mycards(message: types.Message, user: User):
    text = [
        _("List of your lots:"),
        *[
            _("lot_id={id}, {name}, price: {price}").format(
                id=lot.id, name=item.name, price=lot.price
            )
            for lot, item in await join(Lot, Item)
            .select()
            .where(Lot.user_id == user.id)
            .gino.all()
        ],
    ]
    await message.answer("\n".join(text))
