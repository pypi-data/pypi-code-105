import json
from datetime import date
from typing import Dict, List, Optional, Union
from uuid import uuid4

from django.test.client import Client as _Client

from uboxadmin.models.system import User
from uboxadmin.utils import merge_dicts


class Client:
    def __init__(
        self,
        username: str,
        password: str,
    ) -> None:
        self.cli = _Client()
        self.username = username
        self.password = password
        self.headers = {"content_type": "application/json"}
        self.login()

    @classmethod
    def register(cls, username: str, password: str):
        user = User(username=username, create_time=date.today(), update_time=date.today())
        user.set_password(password)
        user.save()

        return cls(username, password)

    @classmethod
    def admin(cls):
        user, _ = User.objects.get_or_create(username="admin", password="123456")
        user.set_password("123456")
        user.save()

        return cls("admin", "123456")

    def login(self):
        resp = _Client().post(
            "/api/admin/base/open/login",
            json.dumps(
                {
                    "username": "admin",
                    "password": "123456",
                    "captchaId": str(uuid4()),
                    "verifyCode": "1234",
                }
            ),
            **self.headers,
        )
        assert resp.status_code == 200, resp.json()
        self.token = resp.json()["data"]["token"]
        self.headers["HTTP_AUTHORIZATION"] = self.token

    def get(self, path: str, headers: Optional[Dict[str, str]] = None):
        if not headers:
            headers = {}

        return self.cli.get(path, **merge_dicts(self.headers, headers))

    def post(self, path: str, data: Optional[Union[Dict, List]] = None, headers: Optional[Dict[str, str]] = None):
        if not headers:
            headers = {}

        if data:
            return self.cli.post(path, json.dumps(data), **merge_dicts(self.headers, headers))
        return self.cli.post(path, **self.headers)

    def post_raw(self, path: str, data: Optional[Union[Dict, List]] = None, headers: Optional[Dict[str, str]] = None):
        if not headers:
            headers = {}

        if data:
            return self.cli.post(path, data, **merge_dicts(self.headers, headers))
        return self.cli.post(path, **self.headers)
