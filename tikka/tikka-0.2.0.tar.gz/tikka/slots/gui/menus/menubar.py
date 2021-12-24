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

import builtins
from typing import TYPE_CHECKING, TypeVar

import wx

from tikka.adapters.repository.preferences import Sqlite3PreferencesRepository
from tikka.adapters.repository.tabs import Sqlite3TabRepository
from tikka.domains.application import Application
from tikka.domains.entities.constants import DATA_PATH
from tikka.slots.gui.menus.accounts import AccountsMenu
from tikka.slots.gui.menus.help import HelpMenu

if TYPE_CHECKING or __name__ == "__main__":
    from tikka.slots.gui.main_window import MainWindow

if TYPE_CHECKING:
    import _

builtins.__dict__["_"] = wx.GetTranslation

MainWindowType = TypeVar("MainWindowType", bound="MainWindow")


class MenuBar(wx.MenuBar):
    def __init__(
        self, main_window: MainWindowType
    ):  # pylint: disable=redefined-outer-name
        """
        Init menubar with main_window

        :param main_window: MainWindow instance
        """
        super().__init__()

        self.Append(
            AccountsMenu(main_window),
            _("&Accounts"),  # pylint: disable=used-before-assignment
        )
        self.Append(HelpMenu(main_window), _("&Help"))


if __name__ == "__main__":
    # create gui application
    wx_app = wx.App()
    # create domain application
    application = Application(DATA_PATH)
    # gui dependencies
    tab_repository = Sqlite3TabRepository(application.sqlite3_client)
    preferences_repository = Sqlite3PreferencesRepository(application.sqlite3_client)
    # create gui
    main_window = MainWindow(None, application)

    menuBar = MenuBar(main_window)

    # Give the menu bar to the frame
    main_window.SetMenuBar(menuBar)

    main_window.Show()
    wx_app.MainLoop()
