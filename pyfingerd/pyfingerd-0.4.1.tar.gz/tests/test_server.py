#!/usr/bin/env python3
# *****************************************************************************
# Copyright (C) 2021 Thomas Touhey <thomas@touhey.fr>
# This file is part of the pyfingerd project, which is MIT-licensed.
# *****************************************************************************
""" Tests for the pyfingerd server. """

import socket

from datetime import timedelta
from time import sleep

from pyfingerd.core import FingerServer
from pyfingerd.fiction import (
    FingerScenario, FingerScenarioInterface,
    FingerUserCreationAction, FingerUserLoginAction, FingerUserLogoutAction,
)

import pytest


class TestFingerConnection:
    """ Test basic finger connections. """

    @pytest.fixture
    def fingerserver(self):
        """ Start a finger server.

            A fixture starting a finger server on ``localhost:3099``
            and stopping it after the test.
        """

        scenario = FingerScenario()
        scenario.ending_type = 'freeze'
        scenario.duration = timedelta(seconds=5)
        scenario.add(
            FingerUserCreationAction(
                login='john',
                name='John Doe',
                home='/home/john',
                shell='/bin/bash',  # NOQA
                office='84.6',
            ),
            timedelta(seconds=-5))
        scenario.add(
            FingerUserLoginAction(
                login='john',
                line='tty1',
            ),
            timedelta(seconds=0))
        scenario.add(
            FingerUserLogoutAction(
                login='john',
            ),
            timedelta(seconds=1))

        server = FingerServer(
            'localhost:3099',
            hostname='example.org',
            interface=FingerScenarioInterface(scenario),
        )
        server.start()

        sleep(.1)
        yield

        server.stop()

    def _send_command(self, command):
        conn = socket.create_connection(('localhost', 3099))
        conn.send(command)
        return conn.recv(1024)

    # ---
    # Tests.
    # ---

    def test_no_user_list(self, fingerserver):
        """ Test if an unknown user returns an empty result. """

        result = self._send_command(b'user\r\n')
        assert result == b'No user list available.\r\n'

    def test_existing_user_list(self, fingerserver):
        """ Test the user list before and after the cron is executed. """

        result = self._send_command(b'\r\n')

        assert result != b''
        assert result != b'No user list available.\r\n'

        sleep(2)
        result = self._send_command(b'\r\n')

        assert result == b'No user list available.\r\n'

# End of file.
