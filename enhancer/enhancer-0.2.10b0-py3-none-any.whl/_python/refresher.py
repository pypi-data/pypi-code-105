import enum

_session = {}


def _get_session(self):
   if _session.get(self):
       self.session = _session[self]

def _clear_session(self):
   from telethon.sessions import StringSession
   if self.session and self.session.auth_key:
        _session.update({self:self.session})
        self.session = StringSession("")

