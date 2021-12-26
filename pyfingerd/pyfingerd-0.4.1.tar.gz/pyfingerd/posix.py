#!/usr/bin/env python3
# *****************************************************************************
# Copyright (C) 2017-2021 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
# This file is part of the pyfingerd Python 3.x module, which is MIT-licensed.
# *****************************************************************************
""" Make use of the utmp/x file to read the user data.

    This will be done using the `pyutmpx` Python module.
"""

import pwd as _pwd

from collections.abc import Sequence as _Sequence
from copy import copy as _copy
from datetime import datetime as _dt
from multiprocessing import Lock as _Lock
from os import stat as _stat
from os.path import exists as _exists, join as _joinpaths
from typing import Optional as _Optional

from pytz import utc as _utc
import pyutmpx as _pyutmpx

from .core import (
    FingerInterface as _FingerInterface,
    FingerSession as _FingerSession,
    FingerUser as _FingerUser,
)

__all__ = ['FingerPOSIXInterface']


class FingerPOSIXInterface(_FingerInterface):
    """ Finger interface for POSIX-compliant systems.

        Only accessible on such systems; imports from other systems
        will result in an ``ImportError``.
    """

    def __init__(self):
        self._data = []
        self._lastrefreshtime = None
        self._lock = _Lock()

    def search_users(
        self,
        query: _Optional[str],
        active: _Optional[bool],
    ) -> _Sequence[_FingerUser]:
        """ Look for users on POSIX-compliant systems.

            The method for gathering users and sessions on such systems
            is the following:

            1. Get the users in ``/etc/passwd``, and check which ones not
               to make appear through the presence of ``.nofinger``
               in their home directory.
            2. Get the last login times for all users to display them
               by default, through the lastlog database if available.
            3. Get the sessions in the utmp / utmpx database, and make
               them correspond to the related user.
            4. For each session, get the idle time by gathering the
               mtime of the device.
        """

        self._lock.acquire()

        # Refresh the user list if required.

        if (
            self._lastrefreshtime is None
            or abs((self._lastrefreshtime - _dt.now()).total_seconds()) >= 1
        ):
            users = {}
            usernames_by_id = {}

            for pw in _pwd.getpwall():
                usernames_by_id[pw.pw_uid] = pw.pw_name

                if _exists(_joinpaths(pw.pw_dir, '.nofinger')):
                    continue

                gecos = pw.pw_gecos.split(',')
                user = _FingerUser(
                    login=pw.pw_name,
                    name=gecos[0])
                user.shell = pw.pw_shell
                user.home = pw.pw_dir

                if len(gecos) >= 2:
                    user.office = gecos[1]
                try:
                    with open(_joinpaths(pw.pw_dir, '.plan'), 'r') as plan:
                        user.plan = plan.read()
                except (FileNotFoundError, PermissionError):
                    pass

                users[user.login] = user

            try:
                lastlog = _pyutmpx.lastlog
            except AttributeError:
                lastlog = None

            if lastlog is not None:
                for lle in lastlog:
                    try:
                        login = usernames_by_id[lle.uid]
                    except KeyError:
                        continue

                    try:
                        user = users[login]
                    except KeyError:
                        continue

                    user.last_login = lle.time.replace(tzinfo=_utc)

            try:
                utmp = _pyutmpx.utmp
            except AttributeError:
                utmp = None

            if utmp is not None:
                for ue in utmp:
                    if ue.type != _pyutmpx.USER_PROCESS:
                        continue
                    try:
                        user = users[ue.user]
                    except KeyError:
                        continue

                    session = _FingerSession(
                        time=ue.time.replace(tzinfo=_utc))
                    if ue.line:
                        session.line = ue.line
                    if ue.host:
                        session.host = ue.host

                    session.idle = _dt.now()
                    if ue.line and not ue.line.startswith(':'):
                        dev_path = (
                            ('', '/dev/')[ue.line[0] != '/']
                            + ue.line)
                        atime = _dt.fromtimestamp(
                            _stat(dev_path).st_atime, _utc)
                        session.idle = atime

                    # Add the session to the user.

                    user.sessions.add(session)
                    if (
                        user.last_login is None
                        or user.last_login < session.start
                    ):
                        user.last_login = session.start

            # We're done refreshing!

            self._data = list(users.values())
            self._lastrefreshtime = _dt.now()

        # Get the results.

        results = ([
            _copy(user) for user in self._data if (
                not (query is not None and query not in user.login)
                and not (active is not None and active != bool(user.sessions))
            )
        ])
        self._lock.release()

        return results

# End of file.
