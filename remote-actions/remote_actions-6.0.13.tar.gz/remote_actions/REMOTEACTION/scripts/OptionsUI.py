"""
The Remote Actions Options UI allows you to change the options of and
check on the usage information for the current company.
"""
try:
    from accpac import *
except ImportError:
    pass

import sys
import datetime
import traceback
import subprocess

from remote_actions import get_token, get_logger, debug_enabled, ADMIN_USER
from remote_actions.services.fleeting_forms import NamespaceClient

DEBUG = False
NAME = "Remote Action Options"
VERSION = '6.0.13'
logger = None

## Entry point

def main(args):
    global logger
    global DEBUG
    DEBUG = debug_enabled()
    logger = get_logger("optionsui")
    if user != ADMIN_USER:
        ui = UI()
        ui.show()
        _alert("Only {} can run {}.".format(ADMIN_USER, NAME))
        ui.closeUI()
    else:
        RemoteActionsUI()

### Utility Functions

def _debug(msg, excinfo=None):
    if DEBUG:
        message = "DEBUG {}\n{}\n---------\n{}".format(rotoID, NAME, msg)
        if excinfo:
            message = "\n".join([message, traceback.format_exc(), ])
        showMessageBox(message)
        logger.debug(msg)

def _alert(msg):
    showMessageBox("{}\n\n{}".format(NAME, msg))
    logger.info(msg)

def success(*args):
    if sum(args) > 0:
        return False
    return True

### Interface Definition

class RemoteActionsUI(UI):
    """UI for Remote Actions management."""

    # Custom control constants
    BUTTON_WIDTH = 1265
    BUTTON_SPACE = 150

    # Grid layout
    COL_MONTH = 0
    COL_USAGE = 1

    def _prompt_user_for_token(self, message):
        """Prompt the user for a token.

        This is used on startup if no token is set for the current company.

        :param message: text to display to the user before opening the UI.
        :type message: str
        :returns: None
        """
        _alert(message)
        openExtenderUI('REMOTEACTION.TokenUI', "", True)

    def __init__(self):
        """Initialize a new UI instance.  Speaks."""
        UI.__init__(self)
        shown = False
        self.title = "Remote Actions Options"
        try:
            self.token = get_token()
            if not self.token:
                self._prompt_user_for_token(
                        "No token set but one is required to continue. "
                        "The token management screen will now open, "
                        "input your unique token there.")

            self.namespace_client = NamespaceClient()
            self.namespaces = self.namespace_client.list()
            if not self.namespaces:
                self._prompt_user_for_token(
                    "Couldn't find any namespace for the configured token. "
                    "Please update the token now.")
                self.namespaces = self.namespace_client.list()

            if not self.namespaces:
                raise Exception("There are no namespaces for the "
                                "configured token.")

            self.namespace = self.namespaces[0]
            self.createScreen()
            self.show()
            shown = True
            self._refresh_grid()
        except Exception as e:
            if not shown:
                self.show()
            _alert("Error starting up: {}".format(
                e))
            _debug(e, excinfo=sys.exc_info()[2])
            self.closeUI()
        else:
            self.onClose = self.onCloseClick
            _debug("version {} started with namespace {}.".format(
                    VERSION, self.namespace['subdomain']))

    def createScreen(self):
        """Configure and render the fields and buttons.
        | Namespace subdomain.ff.io             |
        |                                       |
        | Soft Limit: NNNNNNNN                  |
        | Hard Limit: NNNNNNNN                  |
        |                                       |
        | Remaining this Month: NNNNNN          |
        |                                       |
        | Logo:  [https://path/logo.png       ] |
        | Style: [https://path/style.png      ] |
        |                                       |
        || Period   |                  Usage   ||
        || 2019-12  |                  15456   ||
        || 2020-01  |                  16765   ||
        |                                       |
        |                    +Save      +Close  |
        """
        f = self.addUIField("namespaceLabel")
        f.controlType = "EDIT"
        f.size = 250
        f.width = 5000
        f.labelWidth = 60
        f.caption = "Namespace"
        f.hasFinder = False
        f.setValue("{}.fleetingforms.io".format(self.namespace['subdomain']))
        f.enabled = False
        self.namespace_field = f

        f = self.addUIField("softLimitLabel")
        f.controlType = "EDIT"
        f.size = 250
        f.width = 5000
        f.labelWidth = 60
        f.caption = "Soft Limit"
        f.hasFinder = False
        f.setValue(str(self.namespace['soft_limit']))
        f.enabled = False
        self.soft_limit_field = f

        f = self.addUIField("hardLimitLabel")
        f.controlType = "EDIT"
        f.size = 250
        f.width = 5000
        f.labelWidth = 60
        f.caption = "Hard Limit"
        f.hasFinder = False
        f.setValue(str(self.namespace['hard_limit']))
        f.enabled = False
        self.hard_limit_field = f

        f = self.addUIField("remainingLabel")
        f.controlType = "EDIT"
        f.size = 250
        f.width = 5000
        f.labelWidth = 60
        f.caption = "Remaining (Month)"
        f.hasFinder = False
        curmonth = datetime.datetime.now().strftime("%Y-%m")
        f.enabled = False
        f.setValue(str(self.namespace['soft_limit'] -
                   self.namespace['usage'].get(curmonth, 0)))
        self.remaining_field = f

        f = self.addUIField("supportEmailField")
        f.controlType = "EDIT"
        f.size = 250
        f.width = 5000
        f.labelWidth = 60
        f.caption = "Support Email"
        f.setValue(self.namespace.get('support_email', ''))
        f.hasFinder = False
        self.support_email_field = f

        f = self.addUIField("logoUrlField")
        f.controlType = "EDIT"
        f.size = 250
        f.width = 7500
        f.labelWidth = 60
        f.caption = "Logo URL"
        f.setValue(self.namespace.get('logo', ''))
        f.hasFinder = False
        self.logo_field = f

        f = self.addUIField("styleUrlField")
        f.controlType = "EDIT"
        f.size = 250
        f.width = 7500
        f.labelWidth = 60
        f.caption = "Style URL"
        f.setValue(self.namespace.get('style', ''))
        f.hasFinder = False
        self.style_field = f

        grid = self.addGrid("usageGrid")

        grid.setOnBeginEdit(self.gridOnBeginEdit)
        grid.onRowChanged = self.gridOnRowChanged

        grid.height = -100
        grid.width = -150
        # grid.top = self.remaining_label.top + 150
        grid.addTextColumn("Month", "LEFT", 100, True)
        grid.addTextColumn("Requests", "Right", 300, True)
        self.usage_grid = grid
        self.usage_grid.removeAllRows()

        btn = self.addButton("btnSave", "&Save")
        btn.top = - self.BUTTON_SPACE - btn.height
        btn.width = self.BUTTON_WIDTH
        btn.left = self.usage_grid.left
        btn.onClick = self.onSaveClick
        self.btnSave = btn

        btn = self.addButton("btnToken", "&Token")
        btn.top = - self.BUTTON_SPACE - btn.height
        btn.width = self.BUTTON_WIDTH
        btn.left = self.btnSave.left + self.BUTTON_SPACE + self.BUTTON_WIDTH
        btn.onClick = self.onTokenClick
        self.btnSave = btn

        btn = self.addButton("btnClose", "&Close")
        btn.top = - self.BUTTON_SPACE - btn.height
        btn.width = self.BUTTON_WIDTH
        btn.left = -self.BUTTON_SPACE - self.BUTTON_WIDTH
        btn.onClick = self.onCloseClick
        self.btnClose = btn

        self.usage_grid.height = -self.BUTTON_SPACE - btn.height - 75

    def gridOnBeginEdit(self, e):
        _alert("Items in this grid cannot be edited.")
        return Abort

    def gridOnRowChanged(self, new_row):
        return Continue

    def _refresh_grid(self):
        for month, usage in self.namespace['usage'].items():
            row = self.usage_grid.createRow()
            row.columns[self.COL_MONTH] = month
            row.columns[self.COL_USAGE] = str(usage)
            self.usage_grid.addRow(row)

    def onSaveClick(self):
        if not hasattr(self, 'namespace') or not self.namespace:
            return Continue

        logo = self.logo_field.getValue()
        style = self.style_field.getValue()
        support_email = self.support_email_field.getValue()

        data = {
            'id': self.namespace['id'],
            'subdomain': self.namespace['subdomain'],
            'support_email': support_email,
            'logo': logo,
            'style': style,
        }

        try:
            self.namespace_client.update(self.namespace['id'],
                                         data=data)
            _alert("Remote Actions settings updated.")
        except Exception as e:
            _alert("Remote Actions settings update failed: {}".format(e))
            logger.exception("namespace {} update failed: {}".format(
                    self.namespace['id'], e))

        return Continue

    def onTokenClick(self):
        openExtenderUI('REMOTEACTION.TokenUI', "", True)

    def onCloseClick(self):
        """Close the UI if the Close button or window X are clicked."""
        self.closeUI()

