# Copyright 2021 Vincent Texier <vit@free.fr>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gettext
from pathlib import Path

from tikka.adapters.config import Config
from tikka.adapters.repository.accounts import Sqlite3AccountRepository
from tikka.adapters.repository.preferences import Sqlite3PreferencesRepository
from tikka.adapters.repository.sqlite3 import Sqlite3Client
from tikka.adapters.repository.tabs import Sqlite3TabRepository
from tikka.adapters.wallets import Wallets
from tikka.domains.accounts import Accounts
from tikka.domains.entities.constants import LOCALES_PATH


class Application:
    translator = None

    def __init__(self, data_path: Path):
        """
        Init application

        :param data_path: Path instance of application data folder
        """

        # data
        self.data_path = data_path

        # dependency injection
        # init config adapter
        self.config = Config(self.data_path)
        # init wallets adapter
        self.wallets = Wallets()
        # database adapter
        self.sqlite3_client = Sqlite3Client(self.config.get("currency"), self.data_path)
        # repositories
        account_repository = Sqlite3AccountRepository(self.sqlite3_client)
        self.tab_repository = Sqlite3TabRepository(self.sqlite3_client)
        self.preferences_repository = Sqlite3PreferencesRepository(self.sqlite3_client)

        # init translation
        self.init_i18n()
        # init Accounts domain
        self.accounts = Accounts(
            account_repository, self.wallets, self.config.get("language")
        )

    def init_i18n(self):
        """
        Init translator from configured language

        :return:
        """
        # define translator for configurated language
        self.translator = gettext.translation(
            "application",
            str(LOCALES_PATH),
            languages=[self.config.get("language")],
        )
        # init translator
        self.translator.install()

    def select_currency(self, currency: str):
        """
        Change currency

        :return:
        """
        if self.config is None:
            raise NoConfigError

        self.config.set("currency", currency)

        if self.sqlite3_client is not None:
            self.sqlite3_client.connection.close()

        # init database connection
        self.sqlite3_client = Sqlite3Client(self.config.get("currency"), self.data_path)

        # create new repository adapters on the new database
        self.accounts.repository = Sqlite3AccountRepository(self.sqlite3_client)
        self.tab_repository = Sqlite3TabRepository(self.sqlite3_client)
        self.preferences_repository = Sqlite3PreferencesRepository(self.sqlite3_client)
        # init account list from new repository adapter
        self.accounts.init_accounts()

    def select_language(self, language: str):
        """
        Select GUI language

        :param language: Code of language (ex: "en_US", "fr_FR")
        :return:
        """
        if self.config is None:
            raise NoConfigError

        self.config.set("language", language)
        self.init_i18n()


class NoDatabaseError(Exception):
    pass


class NoConfigError(Exception):
    pass
