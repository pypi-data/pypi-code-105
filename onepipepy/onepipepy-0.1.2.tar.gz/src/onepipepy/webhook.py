from .errors import UnAuthorizedWebhook
from .models import *


class Added(object):
    def __init__(self, webhook):
        self.webhook = webhook
        self.obj = self.webhook.event_obj[1]
        current = self.webhook.json_data.get("current", dict())
        setattr(self, self.obj, globals()[self.obj](**current))


class Updated(object):
    def __init__(self, webhook):
        self.webhook = webhook
        self.obj = self.webhook.event_obj[1]
        current = self.webhook.json_data.get("current", dict())
        previous = self.webhook.json_data.get("previous", dict())
        for key in current.keys():
            if current.get(key, None) != previous.get(key, None):
                self.change = dict(
                    key=key,
                    current_value=current[key],
                    previous_value=previous[key]
                )
                break
        setattr(self, "current_" + self.obj, globals()[self.obj](**current))
        setattr(self, "previous_" + self.obj, globals()[self.obj](**previous))


class Merged(object):
    def __init__(self, webhook):
        self.webhook = webhook


class Deleted(object):
    def __init__(self, webhook):
        self.webhook = webhook


class Webhook(object):
    def __init__(self, *args, **kwargs):
        webhook_auth = kwargs.get("webhook_auth", None)
        if webhook_auth is not None:
            self.username = webhook_auth.get("username")
            self.password = webhook_auth.get("password")
            self.auth()
        self.request = args[0]
        self.json_data = self.request.get_json(force=True)
        self.event_obj = self.json_data["event"].split(".")
        setattr(self, self.event_obj[0], globals()[self.event_obj[0]](self))

    def auth(self):
        auth = self.request.authorization
        if auth is None:
            raise UnAuthorizedWebhook
        if auth["username"] != self.username and auth["password"] != self.password:
            raise UnAuthorizedWebhook

