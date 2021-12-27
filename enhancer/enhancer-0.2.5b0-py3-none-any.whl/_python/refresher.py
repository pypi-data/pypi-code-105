import enum

_session = {}


class _dummy:
    def _get_session(self):
        if _session.get(self):
            self.session = _session[self]

    def _clear_session(self):
        from telethon.sessions import StringSession
        _session.update({self:self.session})
        self.session = StringSession("")

enum._make_class_unpicklable(_dummy)
