# from typing import List, Union
#
# from aiogram import types
# from aiogram.dispatcher.filters.state import default_state
#
# from app.messages import MESSAGES
# from app.misc import dp
# from app.utils.states import States
#
#
# def _parse_upload(
#     raw_text: str,
#     user_id: int,
#     row_delimiter="\n",
#     column_delimiter=",",
#     trim_carriage_return=True,
# ) -> Union[List[Item], None]:
#     result = []
#     if trim_carriage_return:
#         raw_text = raw_text.replace("\r", "")
#     rows = raw_text.split(row_delimiter)
#     for a in [row.split(column_delimiter) for row in rows]:
#         if len(a) != 2:
#             result = None
#             break
#         else:
#             result.append(Item(user_id, name=a[0], price=a[1]))
#     return result
#
#
# @dp.message_handler(commands=["upload"], state=default_state)
# async def upload_command(message: types.Message):
#     await message.reply(MESSAGES["upload"])
#     await States.UPLOAD.set()
#
#
# @dp.message_handler(state=States.UPLOAD)
# async def upload_parse_rows(message: types.Message):
#     user = db.get_user(message.from_user.id)
#     upload_records = _parse_upload(message.text, user.id)
#     if not upload_records:
#         await message.reply(MESSAGES["upload_parse_failed"])
#         await States.UPLOAD.set()
#         return
#     user_items = db.get_user_items(message.from_user.id)
#     if len(upload_records) + len(user_items) > user.limit:
#         await message.reply(
#             MESSAGES["upload_limit_exceeded"].format(user.limit, message.text)
#         )
#         await default_state.set()
#         return
#     for item in upload_records:
#         db.insert(item)
#     await message.reply(MESSAGES["upload_complete"])
#     await default_state.set()
