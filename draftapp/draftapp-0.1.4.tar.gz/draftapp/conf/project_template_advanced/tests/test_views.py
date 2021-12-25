# -*- coding: utf-8 -*-
from project_name.config import config
from unittest.mock import patch, MagicMock

base_url = config.get("flask", "base_url")


def test_ping(client):
    """test case for create resource operation"""
    response = client.get(f"{base_url}/v1/ping")
    assert response.status_code == 200


def test_ping_failure(client):
    """test case for create resource operation"""
    response = client.get(f"/v1/ping")
    data = response.get_data()
    assert b'Please re-verify the URL. Check if context path is present' == data
