from abc import abstractmethod


class ObjectsListMixin:
    _list_mixin_header = ""
    _row_delimiter = "\n"

    @abstractmethod
    def row_repr(self):
        """Get row repr"""
        raise NotImplementedError

    @classmethod
    def list_repr(cls, list_):
        reply_text = cls._list_mixin_header
        for row in list_:
            reply_text += row.row_repr() + cls._row_delimiter
        return reply_text
