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
from wx import dataview

from tikka.domains.application import Application
from tikka.domains.entities.account import Account
from tikka.domains.entities.constants import DATA_PATH
from tikka.domains.entities.pubkey import PublicKey
from tikka.slots.gui.entities.constants import LOCKED_IMAGE, UNLOCKED_IMAGE
from tikka.slots.gui.images import images
from tikka.slots.gui.menus.account_popup import AccountPopupMenu

if TYPE_CHECKING or __name__ == "__main__":
    from tikka.slots.gui.main_window import MainWindow
if TYPE_CHECKING:
    import _

MainWindowType = TypeVar("MainWindowType", bound="MainWindow")

builtins.__dict__["_"] = wx.GetTranslation


class AccountListWindow(wx.Frame):
    def __init__(self, parent: MainWindowType):
        """
        Init accounts list window

        :param parent: Instance of parent widget
        """
        super().__init__(parent)

        self.SetTitle(_("Account list"))  # pylint: disable=used-before-assignment
        self.SetSize(600, 300)

        locked_image = images.load(LOCKED_IMAGE)
        locked_image.Rescale(25, 25, wx.IMAGE_QUALITY_HIGH)
        self.locked_bitmap = locked_image.ConvertToBitmap()
        unlocked_image = images.load(UNLOCKED_IMAGE)
        unlocked_image.Rescale(25, 25, wx.IMAGE_QUALITY_HIGH)
        self.unlocked_bitmap = unlocked_image.ConvertToBitmap()

        # create the listctrl
        self.account_listctrl = dataview.DataViewListCtrl(
            self,
            wx.ID_ANY,
            size=(600, 300),
            style=dataview.DV_SINGLE,
        )
        col00 = self.account_listctrl.AppendBitmapColumn(_(" "), 0, width=25)
        col00.SetSortable(sortable=True)
        col01 = self.account_listctrl.AppendTextColumn(_("Public key"), width=450)
        col01.SetSortable(sortable=True)

        self.reset_listctrl()

        sizer = wx.BoxSizer(orient=wx.VERTICAL)
        sizer.Add(self.account_listctrl, flag=wx.ALL | wx.EXPAND, border=10)
        self.SetSizerAndFit(sizer)

        # bind events
        self.Bind(
            dataview.EVT_DATAVIEW_ITEM_CONTEXT_MENU,
            lambda event: self._right_click(),
            self.account_listctrl,
        )
        self.account_listctrl.Bind(
            wx.EVT_LEFT_DCLICK, lambda event: self._select_item()
        )
        self.Bind(wx.EVT_CLOSE, lambda event: self._close(), self)

        # expose listbox window instance in main window
        self.GetParent().account_list_window = self  # type: ignore

    def _select_item(self):
        """
        Select item in DataviewListCtrl handler

        :return:
        """
        if (
            self.account_listctrl.GetItemCount() == 0
            or self.account_listctrl.GetSelectedItemsCount() == 0
        ):
            return
        # get selected index from listbox
        index = self.account_listctrl.GetSelectedRow()

        # get account from application
        account = self.GetParent().application.accounts.get_by_index(index)
        # update GUI
        self.GetParent().select_account(account)  # type: ignore

    def _right_click(self):
        """
        Right click handler
        Display popup menu on listbox

        :return:
        """
        if (
            self.account_listctrl.GetItemCount() == 0
            or self.account_listctrl.GetSelectedItemsCount() == 0
        ):
            return

        account = self.GetParent().application.accounts.list[
            self.account_listctrl.GetSelectedRow()
        ]

        # create popup menu
        popup_menu = AccountPopupMenu(self.GetParent(), account)

        # show popup menu
        self.account_listctrl.PopupMenu(popup_menu)

    def _close(self):
        """
        CloseEvent handler

        :return:
        """
        # tell main_window
        self.GetParent().account_list_window = None  # type: ignore

        # if event.CanVeto():
        #     event.Veto()
        #     return

        self.Destroy()
        # you may also do:  event.Skip()
        # since the default event handler does call Destroy(), too

    def reset_listctrl(self):
        """
        Init list with accounts

        :return:
        """
        self.account_listctrl.DeleteAllItems()
        for account in self.GetParent().application.accounts.list:
            self.add_account(account)

    def update_listctrl(self):
        """
        Update account listbox

        :return:
        """
        row = 0
        for account in self.GetParent().application.accounts.list:
            # set access column
            self.account_listctrl.SetValue(
                self.locked_bitmap
                if account.signing_key is None
                else self.unlocked_bitmap,
                row,
                0,
            )
            row += 1

    def add_account(self, account: Account):
        """
        Update account in listbox

        :return:
        """
        data = [
            self.locked_bitmap if account.signing_key is None else self.unlocked_bitmap,
            str(PublicKey.from_pubkey(account.pubkey)),
        ]
        self.account_listctrl.AppendItem(data)

    def update_account(self, account: Account):
        """
        Update account in listbox

        :return:
        """
        row = self.GetParent().application.accounts.list.index(account)
        # set access column
        self.account_listctrl.SetValue(
            self.locked_bitmap if account.signing_key is None else self.unlocked_bitmap,
            row,
            0,
        )


if __name__ == "__main__":
    # create gui application
    wx_app = wx.App()
    # create domain application
    application = Application(DATA_PATH)
    # create gui
    main_window = MainWindow(None, application)

    _account1 = Account("H5RS687NT622b9LWyjdtR8BuHrAdREn3y5XpuYWkzAMk")
    _account2 = Account("8bcHY29ctBo1jMAeKEXgztynRdPcQzP2bkdtaYVEZnEP")
    _account3 = Account("EstAB2FE17NaWip9vFDjusK7iV1xoufzhRNhvhiicug6")

    application.accounts.list.append(_account1)
    application.accounts.list.append(_account2)
    application.accounts.list.append(_account3)

    AccountListWindow(main_window).Show()

    # start gui event loop
    wx_app.MainLoop()
