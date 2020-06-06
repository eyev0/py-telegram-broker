from abc import abstractmethod

import aiogram
from aiogram.types import InlineKeyboardMarkup


# def _add_attribute(cls, key, value):
#     """add an attribute to an existing declarative class.
#
#     This runs through the logic to determine MapperProperty,
#     adds it to the Mapper, adds a column to the mapped Table, etc.
#
#     """
#
#     if "__mapper__" in cls.__dict__:
#         if isinstance(value, Column):
#             cls.__table__.append_column(value)
#             cls.__mapper__.add_property(key, value)
#         else:
#             type.__setattr__(cls, key, value)
#             cls.__mapper__._expire_memoizations()
#     else:
#         type.__setattr__(cls, key, value)
#
#
# class MessageDeclarativeMeta(type):
#     def __init__(cls, classname, bases, dict_):
#         if "_decl_class_registry" not in cls.__dict__:
#             _as_declarative(cls, classname, cls.__dict__)
#         type.__init__(cls, classname, bases, dict_)
#
#     def __setattr__(cls, key, value):
#         _add_attribute(cls, key, value)
#
#     def __delattr__(cls, key):
#         _del_attribute(cls, key)


class SendMeMixin:
    _section_sep = '\n\n'
    _field_sep = ': '
    _row_sep = '\n'

    _head = ''
    _head_fields = None
    _body = ''
    _body_fields = None
    _foot = ''

    _kb_hide_me = False
    _kb_rows = 0

    def build_fields_section(self, fields_list):
        return self._row_sep.join([x + self._field_sep + getattr(self, x, ' ') for x in fields_list])

    def build_text(self):
        """Build message text"""
        return self._section_sep.join([self._head, self.build_fields_section(self._head_fields),
                                       self._body, self.build_fields_section(self._body_fields),
                                       self._foot])

    def build_media(self):
        """Build media object to send"""

    def build_keyboard(self):
        """Build inline keyboard"""

    def send(self, bot: aiogram.Bot, keyboard=True, media=False):
        """Send entity via bot"""
