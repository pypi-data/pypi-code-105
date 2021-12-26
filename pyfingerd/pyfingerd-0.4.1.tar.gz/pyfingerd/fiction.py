#!/usr/bin/env python3
# *****************************************************************************
# Copyright (C) 2017-2021 Thomas Touhey <thomas@touhey.fr>
# This file is part of the pyfingerd project, which is MIT-licensed.
# *****************************************************************************
""" Definitions for the finger server fiction interface.

    This file contains everything to decode and use the actions file.
"""

import copy as _copy
import logging as _logging
import math as _math
import os.path as _path

from collections import defaultdict as _defaultdict
from collections.abc import Sequence as _Sequence
from datetime import datetime as _dt, timedelta as _td
from enum import Enum as _Enum
from typing import Optional as _Optional, Union as _Union

from .core import (
    FingerInterface as _FingerInterface,
    FingerSession as _FingerSession,
    FingerUser as _FingerUser,
    cron as _cron,
)
from .utils import (
    format_delta as _format_delta,
    logger as _logger,
    make_delta as _make_delta,
    parse_delta as _parse_delta,
)

__all__ = [
    'FictionalFingerSession', 'FictionalFingerUser',
    'FingerAction', 'FingerFictionInterface', 'FingerScenario',
    'FingerScenarioInterface', 'FingerUserCreationAction',
    'FingerUserDeletionAction', 'FingerUserEditionAction',
    'FingerUserLoginAction', 'FingerUserLogoutAction',
    'FingerUserSessionChangeAction',
]

_toml = None

# ---
# Users and sessions for the fictions.
# ---


class FictionalFingerUser(_FingerUser):
    """ Representation of a user on the fictional system.

        Behaves like a :py:class:`pyfingerd.core.FingerUser`.
        For now, there are no modifications from the base class.
    """

    pass


class FictionalFingerSession(_FingerSession):
    """ Representation of an active session for a given user.

        Behaves like a :py:class:`pyfingerd.core.FingerSession`.
        The two main modifications from the base class are the following:

         * Each session has a name, which identifies it. It can be used
           to designate it, allowing outside code to edit and delete the
           session specifically from an outside point of view.
         * Since the actions only allow for setting the user idle or not,
           when the user is active, the idle timestamp is simulated to make
           it seem like the user makes signs of life at an irregular but
           reasonable rate, like when the user often stops typing to think
           or do a task outside of the computer.
    """

    __slots__ = ('_name', '_is_idle', '_idle_last')

    def __init__(self, *args, name=None, is_idle=False, **kwargs):
        super().__init__(*args, **kwargs)

        self._name = None if name is None else str(name)
        self._is_idle = is_idle
        self._idle_last = self.start

    def __repr__(self):
        p = ('name', 'start', 'line', 'host', 'idle_since', 'active_since')
        p = (
            f'{x}={getattr(self, x)!r}'
            for x in p if getattr(self, x) is not None
        )
        return f"{self.__class__.__name__}({', '.join(p)})"

    @property
    def name(self):
        """ Session name. """

        return self._name

    @name.setter
    def name(self, value):
        self._name = None if value is None else str(value)

    @property
    def idle(self):
        """ Idle time (simulated). """

        if self._is_idle:
            return self._idle_last

        now = _dt.now().astimezone()

        # Generate a number of seconds and return it.

        def s(x):
            return _math.sin(x * (_math.pi / 2))

        x = (now - self._idle_last).seconds
        randsecs = int(abs(s(x) + s(x / 4)))

        return now - _td(seconds=randsecs)

    @idle.setter
    def idle(self, value):
        # Does nothing as we manage this time.

        pass

    @property
    def idle_since(self):
        """ Idle since the given time. """

        if not self._is_idle:
            return None
        return self._idle_last

    @idle_since.setter
    def idle_since(self, value):
        self._is_idle = True
        self._idle_last = value

    @property
    def active_since(self):
        """ Active since the given time. """

        if self._is_idle:
            return None
        return self._idle_last

    @active_since.setter
    def active_since(self, value):
        self._is_idle = False
        self._idle_last = value


# ---
# Unchanged global.
# ---

# TODO: Make that ``UnchangedType()`` (or ``type(Unchanged)()``) always
# return Unchanged, like for None and NoneType.


class _UnchangedType:
    def __repr__(self):
        return 'Unchanged'


Unchanged = _UnchangedType()

# ---
# Action description.
# ---


class FingerAction:
    """ Base class for actions in a fiction. """

    pass


class FingerUserCreationAction(FingerAction):
    """ A user has been created.

        :param login: The login of the user that is being created.
        :param name: The initial value for :py:attr:`FictionalFingerUser.name`.
        :param home: The initial value for :py:attr:`FictionalFingerUser.home`.
        :param shell: The initial value for
                      :py:attr:`FictionalFingerUser.shell`.
        :param office: The initial value for
                       :py:attr:`FictionalFingerUser.office`.
        :param plan: The initial value for :py:attr:`FictionalFingerUser.plan`.
    """

    def __init__(
        self,
        login: str,
        name: _Optional[str] = None,
        home: _Optional[str] = None,
        shell: _Optional[str] = None,
        office: _Optional[str] = None,
        plan: _Optional[str] = None,
    ):
        super().__init__()
        self._login = login
        self._name = name
        self._home = home
        self._shell = shell
        self._office = office
        self._plan = plan

    def __repr__(self):
        p = (
            f'{x}={getattr(self, x)!r}'
            for x in ('login', 'name', 'home', 'shell', 'office', 'plan'))
        return f"{self.__class__.__name__}({', '.join(p)})"

    @property
    def login(self) -> str:
        """ The login of the user that is being created. """

        return self._login

    @property
    def name(self) -> _Optional[str]:
        """ The initial value for :py:attr:`FictionalFingerUser.name`. """

        return self._name

    @property
    def home(self) -> _Optional[str]:
        """ The initial value for :py:attr:`FictionalFingerUser.home`. """

        return self._home

    @property
    def shell(self) -> _Optional[str]:
        """ The initial value for :py:attr:`FictionalFingerUser.shell`. """

        return self._shell

    @property
    def office(self) -> _Optional[str]:
        """ The initial value for :py:attr:`FictionalFingerUser.office`. """

        return self._office

    @property
    def plan(self) -> _Optional[str]:
        """ The initial value for :py:attr:`FictionalFingerUser.plan`. """

        return self._plan


class FingerUserEditionAction(FingerAction):
    """ A user has been edited.

        :param login: The login of the user that is being edited.
        :param name: The new value for :py:attr:`FictionalFingerUser.name`;
                     :py:data:`Unchanged` if the property is unchanged.
        :param home: The new value for :py:attr:`FictionalFingerUser.home`;
                     :py:data:`Unchanged` if the property is unchanged.
        :param shell: The new value for :py:attr:`FictionalFingerUser.shell`;
                      :py:data:`Unchanged` if the property is unchanged.
        :param office: The new value for :py:attr:`FictionalFingerUser.office`;
                       :py:data:`Unchanged` if the property is unchanged.
        :param plan: The new value for :py:attr:`FictionalFingerUser.plan`;
                     :py:data:`Unchanged` if the property is unchanged.
    """

    def __init__(
        self,
        login: str,
        name: _Optional[_Union[str, _UnchangedType]] = Unchanged,
        home: _Optional[_Union[str, _UnchangedType]] = Unchanged,
        shell: _Optional[_Union[str, _UnchangedType]] = Unchanged,
        office: _Optional[_Union[str, _UnchangedType]] = Unchanged,
        plan: _Optional[_Union[str, _UnchangedType]] = Unchanged,
    ):
        super().__init__()
        self._login = login
        self._name = name
        self._home = home
        self._shell = shell
        self._office = office
        self._plan = plan

    def __repr__(self):
        p = (
            f'{x}={getattr(self, x)!r}'
            for x in ('login', 'name', 'home', 'shell', 'office', 'plan'))
        return f"{self.__class__.__name__}({', '.join(p)})"

    @property
    def login(self) -> str:
        """ The login of the user that is being edited. """

        return self._login

    @property
    def name(self) -> _Optional[_Union[str, _UnchangedType]]:
        """ The new value for :py:attr:`FictionalFingerUser.name`.

            Is :py:data:`Unchanged` if the property is unchanged.
        """

        return self._name

    @property
    def home(self) -> _Optional[_Union[str, _UnchangedType]]:
        """ The new value for :py:attr:`FictionalFingerUser.home`.

            Is :py:data:`Unchanged` if the property is unchanged.
        """

        return self._home

    @property
    def shell(self) -> _Optional[_Union[str, _UnchangedType]]:
        """ The new value for :py:attr:`FictionalFingerUser.shell`.

            Is :py:data:`Unchanged` if the property is unchanged.
        """

        return self._shell

    @property
    def office(self) -> _Optional[_Union[str, _UnchangedType]]:
        """ The new value for :py:attr:`FictionalFingerUser.office`.

            Is :py:data:`Unchanged` if the property is unchanged.
        """

        return self._office

    @property
    def plan(self) -> _Optional[_Union[str, _UnchangedType]]:
        """ The new value for :py:attr:`FictionalFingerUser.plan`.

            Is :py:data:`Unchanged` if the property is unchanged.
        """

        return self._plan


class FingerUserDeletionAction(FingerAction):
    """ A user has been deleted.

        :param login: The login of the user to delete.
    """

    def __init__(self, login: str):
        super().__init__()
        self._login = login

    def __repr__(self):
        p = (f'{x}={getattr(self, x)!r}' for x in ('login'))
        return f"{self.__class__.__name__}({', '.join(p)})"

    @property
    def login(self) -> str:
        """ The user's login. """

        return self._login


class FingerUserLoginAction(FingerAction):
    """ A user has logged in.

        :param login: The login of the user to edit.
        :param session_name: The name of the session to create.
        :param line: The new value for :py:attr:`FictionalFingerSession.line`.
        :param host: The new value for :py:attr:`FictionalFingerSession.host`.
    """

    def __init__(
        self,
        login: str,
        session_name: _Optional[str] = None,
        line: _Optional[str] = None,
        host: _Optional[str] = None,
    ):
        super().__init__()
        self._login = login
        self._session = session_name
        self._line = line
        self._host = host

    def __repr__(self):
        p = (
            f'{x}={getattr(self, x)!r}'
            for x in ('login', 'session_name')
        )
        return f"{self.__class__.__name__}({', '.join(p)})"

    @property
    def login(self) -> str:
        """ The login of the user to edit. """

        return self._login

    @property
    def session_name(self) -> _Optional[str]:
        """ The name of the session to create. """

        return self._session

    @property
    def line(self) -> _Optional[str]:
        """ The name of the line from which the user has logged in. """

        return self._line

    @property
    def host(self) -> _Optional[str]:
        """ The name of the host from which the user has logged in. """

        return self._host


class FingerUserSessionChangeAction(FingerAction):
    """ A user session has undergone modifications.

        :param login: The login of the user to edit.
        :param session_name: The name of the session to edit.
        :param is_idle: The new value for
                        :py:attr:`FictionalFingerSession.is_idle`;
                        :py:data:`Unchanged` if the property is unchanged.
    """

    def __init__(
        self,
        login: str,
        session_name: _Optional[str] = None,
        idle: _Union[bool, _UnchangedType] = Unchanged,
    ):
        super().__init__()
        self._login = login
        self._session = session_name
        self._idle = bool(idle)

    def __repr__(self):
        p = (
            f'{x}={getattr(self, x)!r}'
            for x in ('login', 'session_name', 'idle')
        )
        return f"{self.__class__.__name__}({', '.join(p)})"

    @property
    def login(self) -> str:
        """ The login of the user to edit. """

        return self._login

    @property
    def session_name(self) -> _Optional[str]:
        """ The name of the session to edit. """

        return self._session

    @property
    def idle(self) -> _Union[bool, _UnchangedType]:
        """ The new value for :py:attr:`FictionalFingerSession.is_idle`.

            Is :py:data:`Unchanged` if the property is unchanged.
        """

        return self._idle


class FingerUserLogoutAction(FingerAction):
    """ A user has logged out.

        :param login: The login of the user to edit.
        :param session_name: The name of the session to delete.
    """

    def __init__(
        self,
        login: str,
        session_name: _Optional[str] = None,
    ):
        super().__init__()
        self._login = login
        self._session = session_name

    def __repr__(self):
        p = (
            f'{x}={getattr(self, x)!r}'
            for x in ('login', 'session_name')
        )
        return f'{self.__class__.__name__}({", ".join(p)})'

    @property
    def login(self) -> str:
        """ The login of the user to edit. """

        return self._login

    @property
    def session_name(self) -> _Optional[str]:
        """ The name of the session to delete. """

        return self._session


# ---
# Base fiction interface.
# ---


class FingerFictionInterface(_FingerInterface):
    """ Base finger fiction interface for managing a scene.

        The basic state for this class is to have no users; it is possible
        at any point in time to apply actions that will add, remove or
        modify users and sessions, using
        :py:meth:`FingerFictionInterface.apply`.

        This class should be subclassed for interfaces specialized in various
        sources for the data; for example, while
        :py:class:`FingerScenarioInterface` is specialized in using a
        static sequence of actions, another class could read events from
        a live source.
    """

    def __init__(self):
        super().__init__()

        # Initialize the object properties.
        # - `users`: the users.
        # - `lasttime`: the last datetime, in order to raise an
        #   exception if not applied in order.

        self._users = {}
        self._lasttime = None

    # ---
    # Expected methods from an interface.
    # ---

    def search_users(
        self,
        query: _Optional[str],
        active: _Optional[bool],
    ) -> _Sequence[FictionalFingerUser]:
        """ Look for users according to a check. """

        return ([
            _copy.deepcopy(user) for user in self._users.values()
            if not (query is not None and query not in user.login)
            and not (active is not None and active != bool(user.sessions))])

    # ---
    # Elements proper to the fiction interface.
    # ---

    def reset(self):
        """ Reset the interface, i.e. revert all actions.

            This method makes the interface return to the original
            state with no users and sessions.
        """

        self._users = {}
        self._lasttime = None

    def apply(self, action, time: _Optional[_dt] = None):
        """ Apply an action to the scene.

            By default, the time of the action is the current time.
        """

        if time is None:
            time = _dt.now().astimezone()

        if self._lasttime is not None and self._lasttime > time:
            raise ValueError("operations weren't applied in order!")

        self._lasttime = time

        if isinstance(action, FingerUserCreationAction):
            # Create user `action.user`.

            if action.login is None:
                raise ValueError('missing login')
            if action.login in self._users:
                raise ValueError('already got a user with that login')

            user = FictionalFingerUser(login=action.login, name=action.name)
            user.shell = action.shell
            user.home = action.home
            user.office = action.office
            user.plan = action.plan

            self._users[user.login] = user
        elif isinstance(action, FingerUserEditionAction):
            # Edit user `action.user` with the given modifications.

            if action.login is None:
                raise ValueError('missing login')
            if action.login not in self._users:
                raise ValueError(
                    f'got no user with login {action.login!r}',
                )

            user = self._users[action.login]
            if action.name is not Unchanged:
                user.name = action.name
            if action.shell is not Unchanged:
                user.shell = action.shell
            if action.home is not Unchanged:
                user.home = action.home
            if action.office is not Unchanged:
                user.office = action.office
            if action.plan is not Unchanged:
                user.plan = action.plan
        elif isinstance(action, FingerUserDeletionAction):
            # Delete user with login `action.login`.

            if action.login is None:
                raise ValueError('missing login')
            if action.login not in self._users:
                raise ValueError(
                    f'got no user with login {action.login!r}',
                )

            del self._users[action.login]
        elif isinstance(action, FingerUserLoginAction):
            # Login as user `action.login` with session `action.session_name`.

            session = FictionalFingerSession(
                time=time,
                name=action.session_name,
            )

            session.line = action.line
            session.host = action.host

            if action.login is None:
                raise ValueError('missing login')

            try:
                user = self._users[action.login]
            except KeyError:
                raise ValueError(
                    f'got no user with login {action.login!r}',
                ) from None

            # We don't check if the session exists or not; multiple
            # sessions can have the same name, we just act on the last
            # inserted one that still exists and has that name.

            user.sessions.add(session)
            if user.last_login is None or user.last_login < session.start:
                user.last_login = session.start
        elif isinstance(action, FingerUserLogoutAction):
            # Logout as user `action.login` from session `action.session_name`.

            if action.login is None:
                raise ValueError('missing login')

            try:
                user = self._users[action.login]
            except KeyError:
                raise ValueError(
                    f'got no user with login {action.login!r}',
                ) from None

            try:
                del user.sessions[action.session_name]
            except (KeyError, IndexError):
                raise ValueError(
                    f'got no session {action.name!r} '
                    f'for user {action.login!r}') from None
        elif isinstance(action, FingerUserSessionChangeAction):
            # Make user with login `action.login` idle.

            if action.login is None:
                raise ValueError('missing login')

            try:
                user = self._users[action.login]
            except KeyError:
                raise ValueError(
                    'got no user with login '
                    f'{action.login!r}',
                ) from None

            try:
                session = user.sessions[action.session_name]
            except (KeyError, IndexError):
                raise ValueError(
                    f'got no session {action.name!r} '
                    f'for user {action.login!r}') from None

            since = time
            if action.idle is Unchanged:
                pass
            elif action.idle:
                session.idle_since = since
            else:
                session.active_since = since


# ---
# Scenario definition and related interface definition.
# ---


class FingerScenario:
    """ Scenario representation for the fictional interface.

        Consists of actions (as instances of subclasses of
        :py:class:`FingerAction`) located at a given timedelta, with
        a given ending type and time.

        A scenario always uses timedeltas and not datetimes, since it can
        start at any arbitrary point in time and some scenarios are even
        on repeat.
    """

    class EndingType(_Enum):
        """ Ending type, i.e. what happens when the scenario comes to an end.

            .. py:data:: FREEZE

                Freeze the end state forever.

            .. py:data:: STOP

                Stop the server as soon as the scenario has reached an end.

            .. py:data:: REPEAT

                Repeat the scenario from the beginning while
                starting again from the initial state.
        """

        FREEZE = 0
        STOP = 1
        REPEAT = 2

    def __init__(self):
        # Initialize the properties.

        self._end_type = None
        self._end_time = None
        self._actions = []

    @property
    def ending_type(self) -> EndingType:
        """ Ending type of the scenario, as an :py:data:`EndingType`. """

        return self._end_type

    @ending_type.setter
    def ending_type(self, value: EndingType) -> None:
        if value is None:
            self._end_type = None
            return

        try:
            value = self.EndingType(value)
        except ValueError:
            try:
                if isinstance(value, str):
                    value = value.casefold()
                value = {
                    None: None,
                    'interrupt': self.EndingType.FREEZE,
                    'freeze': self.EndingType.FREEZE,
                    'stop': self.EndingType.STOP,
                    'repeat': self.EndingType.REPEAT}[value]
            except KeyError:
                raise TypeError(
                    f'invalid value for ending type: {value!r}')

        self._end_type = value

    @property
    def duration(self) -> _Optional[_td]:
        """ Offset of the ending.

            When the offset is reached, any object following
            the scenario should act out the ending type defined
            in :py:attr:`ending_type`.
        """

        return self._end_time

    @duration.setter
    def duration(self, value: _Optional[_Union[_td, str]]) -> None:
        self._end_time = _make_delta(value, allow_none=True)

    def verify(self) -> None:
        """ Verify that the current scenario is valid.

            This function does the following checks on the scenario:

            * The ending type and time (duration) are well defined.
            * Any user edition or deletion event happens when the
              related user exists.
            * Any session creation, edition or deletion happens on
              a user who exists at that point in time.
            * Any session edition or deletion happens when the
              related session exists.

            Any action defined after the ending time is ignored.

            :raise ValueError: if the current scenario is invalid.
        """

        # Check if the ending is well defined.

        if self._end_time is None:
            raise ValueError('ending time (duration) has not been provided')
        if not isinstance(self._end_type, self.EndingType):
            raise ValueError('ending type has not been provided')

        # Check if the events are coherent.

        users = _defaultdict(lambda: False)
        sessions = _defaultdict(lambda: _defaultdict(lambda: 0))

        for time, action, i in self._actions:
            try:
                if time >= self._end_time:
                    # Action will be ignored.

                    pass
                elif isinstance(action, FingerUserCreationAction):
                    if users[action.login]:
                        # The user we're trying to create already exists.

                        raise ValueError(
                            'trying to create user '
                            f'{action.login!r} which already exists')

                    users[action.login] = True
                elif isinstance(action, FingerUserEditionAction):
                    if not users[action.login]:
                        # The user we're trying to edit doesn't exist.

                        raise ValueError(
                            'trying to edit user '
                            f"{action.login!r} while it doesn't exist")
                elif isinstance(action, FingerUserDeletionAction):
                    if action.login not in users:
                        # The user we're trying to delete doesn't exist.

                        raise ValueError(
                            'trying to delete user '
                            f"{action.login!r} while it doesn't exist")

                    del users[action.login]
                    try:
                        del sessions[action.login]
                    except KeyError:
                        pass
                elif isinstance(action, FingerUserLoginAction):
                    if action.login not in users:
                        # The user we're trying to log in as doesn't exist.

                        raise ValueError(
                            'trying to log in as user '
                            f"{action.login!r} which doesn't exist")

                    sessions[action.login][action.session_name] += 1
                elif isinstance(action, FingerUserSessionChangeAction):
                    if sessions[action.login][action.session_name] <= 0:
                        # The user doesn't exist (anymore?) or the session
                        # does not exist.

                        if users[action.login]:
                            raise ValueError(
                                'trying to change non existing '
                                f'session of user {action.login!r}')
                        else:
                            raise ValueError(
                                'trying to change session of '
                                f'non-existing user {action.login!r}')
                elif isinstance(action, FingerUserLogoutAction):
                    if sessions[action.login][action.session_name] <= 0:
                        # The user doesn't exist (anymore?) or the session
                        # does not exist.

                        if users[action.login]:
                            raise ValueError(
                                'trying to delete non existing '
                                f'session of user {action.login!r}')
                        else:
                            raise ValueError(
                                'trying to delete session of '
                                f'non-existing user {action.login!r}')

                    sessions[action.login][action.session_name] -= 1
            except ValueError as e:
                raise ValueError(
                    f'at action #{i} at {_format_delta(time)}: '
                    f'{e!s}',
                ) from None

    @classmethod
    def load(cls, path: str):
        """ Load a scenario from a TOML file.

            Decodes the content of a scenario in TOML format and, if
            successful, returns the result as an instance of FingerScenario.

            :param path: Path of the TOML file to load.
        """

        global _toml

        actions = []
        end_type = None
        end_time = None

        _logger.debug(f'Loading scenario from {path!r}.')

        # Load the required modules.

        if _toml is None:
            try:
                import toml
            except ModuleNotFoundError:
                raise ModuleNotFoundError(
                    "'toml' module required") from None

            _toml = toml
            del toml

        # Read the document and translate all of the timestamps.

        document = _toml.load(path)
        i = 0

        for key in document.keys():
            time = _parse_delta(key)
            if time is None:
                raise ValueError(f'found invalid time: {key!r}')

            if not isinstance(document[key], list):
                raise ValueError(
                    f'time {key!r} is not an array, '
                    f'you have probably written [{key}] instead of '
                    f'[[{key}]]',
                )

            for j, data in enumerate(document[key]):
                try:
                    typ = data['type']

                    if typ in ('interrupt', 'freeze', 'stop', 'repeat'):
                        # Set the ending type and time.

                        if end_time is None or end_time > time:
                            end_type = {
                                'interrupt': cls.EndingType.FREEZE,
                                'freeze': cls.EndingType.FREEZE,
                                'stop': cls.EndingType.STOP,
                                'repeat': cls.EndingType.REPEAT}[typ]
                            end_time = time

                        continue
                    elif typ == 'create':
                        # User creation.

                        plan = None
                        if 'plan' in data:
                            pp = _path.join(_path.dirname(path), data['plan'])
                            plan = open(pp).read()

                        action = FingerUserCreationAction(
                            login=data['login'],
                            name=data.get('name'),
                            shell=data.get('shell'),  # NOQA
                            home=data.get('home'),
                            office=data.get('office'),
                            plan=plan)
                    elif typ == 'update':
                        # User update.

                        plan = Unchanged
                        if 'plan' in data:
                            if data['plan'] is False:
                                plan = None
                            else:
                                pp = _path.join(
                                    _path.dirname(path), data['plan'])
                                plan = open(pp).read()

                        def g(k):
                            if k in data and data[k] is False:
                                return None
                            return data.get(k, Unchanged)

                        action = FingerUserEditionAction(
                            login=data['login'],
                            name=g('name'),
                            shell=g('shell'),  # NOQA
                            home=g('home'),
                            office=g('office'),
                            plan=plan,
                        )
                    elif typ == 'delete':
                        # User deletion.

                        action = FingerUserDeletionAction(
                            login=data['login'])
                    elif typ == 'login':
                        # User login.

                        action = FingerUserLoginAction(
                            login=data['login'],
                            session_name=data.get('session'),
                            line=data.get('line'),
                            host=data.get('host'))
                    elif typ == 'logout':
                        # User logout.

                        action = FingerUserLogoutAction(
                            login=data['login'],
                            session_name=data.get('session'),
                        )
                    elif typ in ('idle', 'active'):
                        # Idle change status.

                        action = FingerUserSessionChangeAction(
                            login=data['login'],
                            session_name=data.get('session'),
                            idle=(typ == 'idle'),
                        )
                    else:
                        raise ValueError(f'invalid action type {typ!r}')

                    actions.append((time, action, i))
                    i += 1
                except Exception as e:
                    raise ValueError(
                        f'at action #{j + 1} at '
                        f'{_format_delta(time)}: {e!s}',
                    ) from None

        # Sort and check the actions.

        _logger.debug(
            f'Loaded {len(actions)} action{("", "s")[len(actions) >= 2]}.',
        )

        if end_type is None:
            # If no ending was given in the script file, we ought to
            # interrupt 10 seconds after the last action.

            try:
                last_time = max(actions, key=lambda x: (x[0], x[2]))[0]
            except ValueError:
                last_time = _td(seconds=0)

            end_type = cls.EndingType.FREEZE
            end_time = last_time + _td(seconds=10)

        scenario = cls()
        scenario.ending_type = end_type
        scenario.duration = end_time
        for time, action, *_ in actions:
            scenario.add(action, time)

        return scenario

    def get(
        self,
        to: _Optional[_td] = None,
        since: _Optional[_td] = None,
    ) -> _Sequence[FingerAction]:
        """ Return a sequence of actions in order from the scenario.

            :param to: Maximum timedelta for the actions to gather.
            :param since: Minimum timedelta for the actions to gather.
            :return: The sequence of actions that occur and respect
                     the given constraints.
        """

        if since is not None and to is not None and since > to:
            raise ValueError(
                f'`since` ({since}) should be before `to` ({to}).')

        for time, action, _ in self._actions:
            if since is not None and since >= time:
                continue
            if to is not None and time > to:
                continue
            if self._end_time is not None and time >= self._end_time:
                continue
            yield time, action

    def add(self, action: FingerAction, time: _Union[_td, str]):
        """ Add an action at the given time to the registered actions. """

        time = _make_delta(time)

        try:
            index = max(x[2] for x in self._actions)
        except ValueError:
            index = 0

        self._actions.append((time, action, index + 1))
        self._actions.sort(key=lambda x: (x[0], x[2]))


class FingerScenarioInterface(FingerFictionInterface):
    """ Fiction interface, to follow actions written in a scenario.

        Subclasses :py:class:`FingerFictionInterface` and adds
        a regular update method for updating the state according
        to the given scenario.

        :param scenario: The scenario to follow using the given interface.
        :param start: The start time at which the scenario is supposed to
                      have started; by default, the current time is used.
    """

    def __init__(
        self,
        scenario: FingerScenario,
        start: _Optional[_dt] = None,
    ):
        """ Initialize the interface. """

        if start is None:
            start = _dt.now()
        if start.tzinfo is None:
            start = start.astimezone()

        super().__init__()

        # Initialize the object properties.

        if not isinstance(scenario, FingerScenario):
            raise TypeError(
                'scenario should be a FingerScenario, '
                f'is {scenario.__class__.__name__}.')

        scenario.verify()
        scenario = _copy.copy(scenario)

        # Initialize the object properties.
        # - `scenario`: the script to follow.
        # - `laststart`: the last registered start.
        # - `lastdelta`: the last registered delta.

        self._scenario = scenario
        self._start = start
        self._laststart = None
        self._lastdelta = None

    @_cron('* * * * * *')
    def update(self):
        """ Update the state according to the scenario every second. """

        now = _dt.now().astimezone()
        start = self._laststart or self._start

        # Check if we have gone back in time, e.g. if the system time
        # has changed, and just start again.

        if self._lastdelta is not None and now < start + self._lastdelta:
            _logger.debug('We seem to have gone back in time!')
            _logger.debug("Let's start again from a clean slate.")

            start = self._start

            self._lastdelta = None
            self.reset()

        # Check if we have reached an ending.

        if now > start + self._scenario.duration:
            ending_type = self._scenario.ending_type
            if ending_type == FingerScenario.EndingType.STOP:
                _logger.debug('Stop ending has been reached.')
                exit()
            elif ending_type == FingerScenario.EndingType.FREEZE:
                delta = self._scenario.duration
            else:
                # We're on 'repeat', so we are going to have a slightly
                # different start because we want the start of the new
                # iteration.
                #
                #     >>> from datetime import (datetime as dt
                #         timedelta as td)
                #     >>> a = dt(2000, 1, 1)
                #     >>> b = a + td(seconds = 27)
                #     >>> (b - a) % td(seconds = 10)
                #     datetime.timedelta(seconds=7)
                #     >>> b - (b - a) % td(seconds = 10)
                #     datetime.datetime(2000, 1, 1, 0, 0, 20)
                #
                # Let's see.

                start = now - (now - start) % self._scenario.duration

                self.reset()
                self._lastdelta = None

                _logger.debug('Repeat ending has been reached.')
                _logger.debug(f'Looping from {start.isoformat()}.')

        # We're within the duration of the fiction, so we just use the
        # offset from the start.

        delta = now - start

        # Then, we apply the actions up to the current time.

        actions = self._scenario.get(to=delta, since=self._lastdelta)

        if _logger.getEffectiveLevel() <= _logging.DEBUG:
            actions = list(actions)
            if actions:
                _logger.debug(
                    f'Applying {len(actions)} '
                    f'action{("", "s")[len(actions) >= 2]}:',
                )
                for time, action in actions:
                    _logger.debug(f' at {_format_delta(time)}: {action!r}')

        for time, action in actions:
            self.apply(action, start + time)

        # Finally, we can keep track of where we were.

        self._laststart = start
        self._lastdelta = delta

# End of file.
