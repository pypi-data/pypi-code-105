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
import sys
from typing import TYPE_CHECKING, Optional, Union

import wx
from wx.aui import AUI_NB_CLOSE_ON_ACTIVE_TAB, AUI_NB_TAB_MOVE, AuiNotebook

from tikka import __version__
from tikka.domains.application import Application
from tikka.domains.entities.account import Account
from tikka.domains.entities.constants import CURRENCIES
from tikka.domains.entities.pubkey import PublicKey
from tikka.domains.entities.tab import Tab
from tikka.domains.interfaces.repository.preferences import SELECTED_TAB_PAGE_KEY
from tikka.slots.gui.menus.menubar import MenuBar
from tikka.slots.gui.tabs.account import AccountPanel

if TYPE_CHECKING:
    pass

builtins.__dict__["_"] = wx.GetTranslation

# supported languages
supported_languages = {
    "en_US": wx.LANGUAGE_ENGLISH,
    "fr_FR": wx.LANGUAGE_FRENCH,
}


class MainWindow(wx.Frame):
    """
    Top level Frame window class
    """

    def __init__(self, parent: Optional[wx.Frame], application: Application):
        """
        Init top level window

        :param parent: Parent window
        :param application: Main Application instance
        """
        super().__init__(parent)

        self.application = application
        self.locale = None
        self.account_list_window = None

        # configuration
        self.update_title()
        self.select_language(self.application.config.get("language"))

        # Add the menu bar to the frame
        self.SetMenuBar(MenuBar(self))

        # create notebook for tabs
        self.notebook = AuiNotebook(
            self, style=AUI_NB_CLOSE_ON_ACTIVE_TAB | AUI_NB_TAB_MOVE
        )
        # init tabs
        self.init_tabs()

        self.SetClientSize(self.notebook.GetBestSize())

        self.SetStatusBar(wx.StatusBar(self))

        # layout
        self.SetSize((800, 600))

        # events
        self.Bind(wx.EVT_CLOSE, lambda event: self._close(), self)

    def _close(self):
        """
        CloseEvent handler

        :return:
        """
        # save tab selection in preferences
        self.application.preferences_repository.set(
            SELECTED_TAB_PAGE_KEY, self.notebook.GetSelection()
        )

        # if event.CanVeto():
        #     event.Veto()
        #     return

        self.Destroy()
        # you may also do:  event.Skip()
        # since the default event handler does call Destroy(),

    def init_tabs(self):
        """
        Init tabs from repository

        :return:
        """
        # delete in GUI
        self.notebook.DeleteAllPages()

        # fetch tabs from repository
        for tab in self.application.tab_repository.list():
            # if account tab...
            if tab.panel_class == AccountPanel.__name__:
                # get account from list
                for account in self.application.accounts.list:
                    if account.pubkey == tab.id:
                        self.add_account_tab(account)

        # get preferences
        preferences_selected_page = self.application.preferences_repository.get(
            SELECTED_TAB_PAGE_KEY
        )
        if preferences_selected_page is not None:
            self.notebook.SetSelection(int(preferences_selected_page))

    def get_account_page_number_by_pubkey(self, pubkey: str) -> Optional[int]:
        """
        Return page number of tab containing account with pubkey

        :param pubkey: Public Key of account
        :return:
        """
        page_number = 0
        page_exists = False

        for count in range(0, self.notebook.GetPageCount()):
            panel = self.notebook.GetPage(count)
            if isinstance(panel, AccountPanel):
                if panel.id == pubkey:  # type AccountPanel
                    page_exists = True
                    break
            page_number += 1

        if page_exists is True:
            return page_number

        return None

    def update_title(self):
        """
        Update window title with version and currency

        :return:
        """
        self.SetTitle(
            "Tikka {version} - {currency}".format(  # pylint: disable=consider-using-f-string
                version=__version__,
                currency=CURRENCIES[self.application.config.get("currency")],
            )
        )

    def add_account(self, account: Account):
        """
        Add account in the list

        :param account: Account instance
        :return:
        """
        if self.account_list_window:
            self.account_list_window.add_account(account)

        self.save_tab(self.add_account_tab(account))

    def add_account_tab(self, account: Account) -> AccountPanel:
        """
        Add an account tab in Notebook

        :param account: Account instance
        :return:
        """
        panel = AccountPanel(self.notebook, account)
        panel.set_account(account)
        self.notebook.AddPage(
            panel,
            PublicKey.from_pubkey(account.pubkey).shorten_checksum,
        )
        self.notebook.SetSelection(self.notebook.GetPageCount() - 1)

        return panel

    def save_tab(self, panel: Union[AccountPanel]):
        """
        Save panel in tab repository

        :param panel: Panel instance
        :return:
        """
        # save tab in repository
        tab = Tab(panel.id, str(panel.__class__.__name__))
        self.application.tab_repository.add(tab)

    def select_account(self, account: Account) -> None:
        """
        Selected account from list

        :param account: Account instance
        :return:
        """
        page_number = self.get_account_page_number_by_pubkey(account.pubkey)

        if page_number is not None:
            self.notebook.SetSelection(page_number)
        else:
            self.add_account_tab(account)
            self.save_tab(self.add_account_tab(account))

    def delete_account(self, account: Account) -> None:
        """
        Delete account from list and tabs

        :param account: Accoun instance
        :return:
        """
        if self.account_list_window:
            self.account_list_window.reset_listctrl()

        self.delete_account_tab(account)

    def delete_account_tab(self, account: Account) -> None:
        """
        Delete an account tab in Notebook

        :param account: Account instance
        :return:
        """
        page_number = self.get_account_page_number_by_pubkey(account.pubkey)
        if page_number is not None:
            panel = self.notebook.GetPage(page_number)
            # delete tab in repository
            self.application.tab_repository.delete(panel.id)
            # delete page in GUI
            self.notebook.DeletePage(page_number)

    def unlock_account(self, account: Account):
        """
        Unlock account event

        :param account: Account instance
        :return:
        """
        page_number = self.get_account_page_number_by_pubkey(account.pubkey)

        if page_number is not None:
            panel = self.notebook.GetPage(page_number)
            # update account panel
            panel.set_unlock_status(account)

        if self.account_list_window:
            # update account in listbox
            self.account_list_window.update_account(account)

    def lock_account(self, account: Account):
        """
        Lock account event

        :param account: Account instance
        :return:
        """
        page_number = self.get_account_page_number_by_pubkey(account.pubkey)

        if page_number is not None:
            panel = self.notebook.GetPage(page_number)
            # update account panel
            panel.set_unlock_status(account)

        if self.account_list_window:
            # update account in listbox
            self.account_list_window.update_account(account)

    def load_wallet(self, account: Account, new: bool):
        """
        Load wallet to create/update account

        :param account: Account instance
        :param new: True if the wallet created a new account, False otherwise
        :return:
        """
        if self.account_list_window:
            if new:
                self.add_account(account)
            else:
                # update account in list
                self.account_list_window.update_account(account)

        page_number = self.get_account_page_number_by_pubkey(account.pubkey)

        if page_number is not None:
            panel = self.notebook.GetPage(page_number)
            # update account tab
            panel.set_account(account)

    def save_wallet(self, account):
        """
        Save wallet of account

        :param account: Account instance
        :return:
        """

    def select_language(self, language: str):
        """
        Update the language to the requested one.

        Make *sure* any existing locale is deleted before the new
        one is created.  The old C++ object needs to be deleted
        before the new one is created, and if we just assign a new
        instance to the old Python variable, the old C++ locale will
        not be destroyed soon enough, likely causing a crash.

        :param language: one of the supported language codes

        """
        # if an unsupported language is requested default to English
        selected_language_code = supported_languages.get(language, wx.LANGUAGE_ENGLISH)

        if self.locale:
            assert sys.getrefcount(self.locale) <= 2
            del self.locale

        # create a locale object for this language
        self.locale = wx.Locale(selected_language_code)
        if self.locale is not None and not self.locale.IsOk():
            self.locale = None

    def select_currency(self):
        """
        :return:
        """
        self.update_title()

        # update list
        if self.account_list_window:
            self.account_list_window.reset_listctrl()

        self.init_tabs()
