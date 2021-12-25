# -*- coding: utf-8 -*-
import pytest

from project_name import application
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="session")
def client():
    client = application.test_client()
    yield client


def create_db_engine():
    """Method to create db engine"""
    return create_engine("sqlite:////tmp/sqlite.db")


def create_db_session(db_engine):
    """create db session method"""
    session_maker = sessionmaker(bind=db_engine)
    return session_maker()


@pytest.fixture()
def session():
    """create db session"""
    db_engine = create_db_engine()
    yield create_db_session(db_engine)


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.delattr("requests.sessions.Session.request")
