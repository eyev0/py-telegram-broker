# import re
# from typing import List, Union
#
# from aiogram import types
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import default_state
#
# from app.messages import MESSAGES
# from app.misc import dp
# from app.utils.states import States
#
#
# def _parse_delete(raw_text: str, user_id: int) -> Union[List, None]:
#     if raw_text == "all":
#         del_records = db.get_user_items(user_id)
#     else:
#         if re.findall("[^0-9, ]", raw_text):
#             return None
#         del_ids = [x.strip() for x in raw_text.split(",")]
#         del_records = db.get_user_items(user_id, ids=del_ids)
#     return del_records or []
#
#
# @dp.message_handler(commands=["delete"], state=default_state)
# async def delete_command(message: types.Message):
#     # save del_ids and request confirmation
#     args: str = message.get_args()
#     context: FSMContext = dp.current_state(
#         user=message.from_user.id, chat=message.chat.id
#     )
#     if len(args) == 0:
#         await message.reply(MESSAGES["delete_help"])
#         await default_state.set()
#         return
#     del_records = _parse_delete(args, message.from_user.id)
#     if del_records is None:
#         await message.reply(MESSAGES["delete_format_error"])
#         await default_state.set()
#         return
#     if not del_records:
#         await message.reply(MESSAGES["delete_no_records"])
#         await default_state.set()
#         return
#     del_str = "\n".join([f"{item.row_repr()}" for item in del_records])
#     await message.reply(MESSAGES["delete_records_confirm"].format(del_str))
#
#     context_data = await context.get_data()
#     context_data["delete_ids"] = ",".join([str(item.id) for item in del_records])
#     await context.set_data(context_data)
#     await States.DELETE.set()
#
#
# @dp.message_handler(
#     lambda m: m.text.strip().lower() in ["да", "yes"], state=States.DELETE
# )
# async def delete_confirm(message: types.Message):
#     # process delete
#     context: FSMContext = dp.current_state(
#         user=message.from_user.id, chat=message.chat.id
#     )
#     context_data = await context.get_data()
#     del_ids = context_data.get("delete_ids", "")
#     del_records = db.get_user_items(message.from_user.id, ids=del_ids)
#     del_str = "\n".join([x.row_repr() for x in del_records])
#     for item in del_records:
#         db.delete(item)
#     reply_text = MESSAGES["delete_records_done"].format(del_str)
#     context_data["delete_ids"] = None
#     await context.set_data(context_data)
#     await message.reply(reply_text)
#     await default_state.set()
