#!/usr/bin/env python3
# *****************************************************************************
# Copyright (C) 2021 Thomas Touhey <thomas@touhey.fr>
# This file is part of the pyfingerd project, which is MIT-licensed.
# *****************************************************************************
""" Tests for the pyfingerd server. """

from pyfingerd.fiction import (
    FingerScenario, FingerUserCreationAction, FingerUserDeletionAction,
    FingerUserEditionAction, FingerUserLoginAction, FingerUserLogoutAction,
)

import pytest


class TestScenarios:
    """ Test scenarios. """

    def test_no_ending_type(self):
        scenario = FingerScenario()
        scenario.duration = '1m'
        with pytest.raises(ValueError, match=r'ending type'):
            scenario.verify()

    def test_no_duration(self):
        scenario = FingerScenario()
        scenario.ending_type = FingerScenario.EndingType.FREEZE
        with pytest.raises(ValueError, match=r'ending time'):
            scenario.verify()

    def test_edit_without_create_user(self):
        scenario = FingerScenario()
        scenario.ending_type = FingerScenario.EndingType.FREEZE
        scenario.duration = '1m'

        scenario.add(
            FingerUserEditionAction(
                login='user',
                shell='/bin/sh',  # NOQA
            ),
            '0s',
        )

        with pytest.raises(ValueError, match=r'trying to edit user'):
            scenario.verify()

    def test_delete_without_create_user(self):
        scenario = FingerScenario()
        scenario.ending_type = FingerScenario.EndingType.FREEZE
        scenario.duration = '1m'

        scenario.add(
            FingerUserDeletionAction(
                login='user',
            ),
            '0s',
        )

        with pytest.raises(ValueError, match=r'trying to delete user'):
            scenario.verify()

    def test_edit_after_delete_user(self):
        scenario = FingerScenario()
        scenario.ending_type = FingerScenario.EndingType.FREEZE
        scenario.duration = '1m'

        scenario.add(
            FingerUserCreationAction(
                login='user',
                shell='/bin/sh',  # NOQA
            ),
            '0s',
        )
        scenario.add(
            FingerUserEditionAction(
                login='user',
                name='John Doe',
            ),
            '10s',
        )
        scenario.add(
            FingerUserDeletionAction(
                login='user',
            ),
            '5s',
        )

        with pytest.raises(ValueError, match=r'trying to edit user'):
            scenario.verify()

    def test_login_without_creation(self):
        scenario = FingerScenario()
        scenario.ending_type = FingerScenario.EndingType.FREEZE
        scenario.duration = '1m'

        scenario.add(
            FingerUserLoginAction(
                login='user',
            ),
            '0s',
        )

        with pytest.raises(ValueError, match=r'trying to log in as'):
            scenario.verify()

    def test_logout_without_creation(self):
        scenario = FingerScenario()
        scenario.ending_type = FingerScenario.EndingType.FREEZE
        scenario.duration = '1m'

        scenario.add(
            FingerUserLogoutAction(
                login='user',
            ),
            '0s',
        )

        with pytest.raises(
            ValueError, match=r'trying to delete session of non-existing',
        ):
            scenario.verify()

    def test_logout_without_login(self):
        scenario = FingerScenario()
        scenario.ending_type = FingerScenario.EndingType.FREEZE
        scenario.duration = '1m'

        scenario.add(
            FingerUserCreationAction(
                login='user',
                shell='/bin/sh',  # NOQA
            ),
            '0s',
        )
        scenario.add(
            FingerUserLogoutAction(
                login='user',
            ),
            '1s',
        )

        with pytest.raises(
            ValueError, match=r'trying to delete non existing session',
        ):
            scenario.verify()

# End of file.
