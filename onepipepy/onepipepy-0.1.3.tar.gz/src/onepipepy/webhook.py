from .errors import UnAuthorizedWebhook
from .models import *


class Added(object):
    def __init__(self, webhook):
        self.webhook = webhook
        setattr(
            self,
            self.webhook.obj,
            self.webhook.json_data.get("current", dict())
        )


class Updated(object):
    def __init__(self, webhook):
        self.webhook = webhook
        self.current = self.webhook.json_data.get("current", dict())
        self.previous = self.webhook.json_data.get("previous", dict())
        for key in self.current.keys():
            if self.current.get(key, None) != self.previous.get(key, None):
                self.change = dict(
                    key=key,
                    current_value=self.current[key],
                    previous_value=self.previous[key]
                )
                break


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
        self.event = self.json_data["event"].split(".")[0].lower()
        self.obj = self.json_data["event"].split(".")[1].lower()
        setattr(self, self.event, globals()[self.event.capitalize()](self))

    def auth(self):
        auth = self.request.authorization
        if auth is None:
            raise UnAuthorizedWebhook
        if auth["username"] != self.username and auth["password"] != self.password:
            raise UnAuthorizedWebhook

