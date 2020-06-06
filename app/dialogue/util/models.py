from abc import abstractmethod


class SendListMixin:
    _num_records = 20
    _list_mixin_header = ''

    @abstractmethod
    def row_repr(self):
        """Get row repr"""

    @classmethod
    def list_repr(cls, list_):
        reply_text = cls._list_mixin_header
        for i in range(min(cls._num_records, len(list_))):
            reply_text += list_[i].row_repr()
        return reply_text
