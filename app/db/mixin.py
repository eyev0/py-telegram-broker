from abc import abstractmethod


class ObjectsListMixin:
    _num_records = 20
    _list_mixin_header = ''
    _row_delimiter = '\n'

    @abstractmethod
    def row_repr(self):
        """Get row repr"""

    @classmethod
    def list_repr(cls, list_):
        reply_text = cls._list_mixin_header
        for i in range(min(cls._num_records, len(list_))):
            reply_text += list_[i].row_repr() + cls._row_delimiter
        return reply_text
