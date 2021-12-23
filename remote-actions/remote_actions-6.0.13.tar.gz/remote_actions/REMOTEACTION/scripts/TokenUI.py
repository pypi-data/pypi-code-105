"""
The Remote Action Token UI allows you to manage the secret Remote Action
Token for the current company.
"""
try:
    from accpac import *
except ImportError as e:
    pass

import re
import traceback

from remote_actions import (set_token, get_token, get_logger,
                            debug_enabled, ADMIN_USER, )
from remote_actions.services.fleeting_forms import NamespaceClient

DEBUG = False
NAME = "Remote Action Token Management"
VERSION = '6.0.13'
logger = None

## Entry point

def main(args):
    global DEBUG
    global logger
    DEBUG = debug_enabled()
    logger = get_logger('tokenui')
    if user != ADMIN_USER:
        ui = UI()
        ui.show()
        _alert("Only {} can run {}.".format(ADMIN_USER, NAME))
        ui.closeUI()
    else:
        RemoteActionTokenUI()

### Utility Functions

def _debug(msg, excinfo=None):
    if DEBUG:
        message = "DEBUG {}\n{}\n---------\n{}".format(rotoID, NAME, msg)
        if excinfo:
            message = "\n".join([message, traceback.format_exc(), ])
        showMessageBox(msg)
        logger.debug(msg)

def _alert(msg):
    showMessageBox("{}\n\n{}".format(NAME, msg))
    logger.info(msg)

def success(*args):
    if sum(args) > 0:
        return False
    return True

### Interface Definition

class RemoteActionTokenUI(UI):
    """UI for Remote action token management.    """

    # Custom control constants
    BUTTON_WIDTH = 1265
    BUTTON_SPACE = 150

    UUID_REGEX = re.compile('^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-'
                            '?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z', re.I)

    def __init__(self):
        """Initialize a new UI instance."""
        UI.__init__(self)
        self.title = "Remote Actions - Token Management"
        self.token = get_token()
        self.createScreen()
        self.show()
        self.onClose = self.onCloseClick

    def obscured_token(self):
        """Get the token for this company but obscure its contents with '*'s.

        :returns: token with characters obscured.
        :rtype: string
        """
        if self.token:
            return re.sub('[a-zA-Z0-9]', '*', self.token, 24)
        return 'unset'

    def createScreen(self):
        """Configure and render the fields and buttons.
        | Token  ______________________________ |
        |                    +Save      +Close  |
        """
        f = self.addUIField("tokenTextField")
        f.controlType = "EDIT"
        f.size = 250
        f.width = 5000
        f.labelWidth = 60
        f.caption = "Token"
        f.hasFinder = False
        f.setValue(self.obscured_token())
        f.enabled = True
        self.token_field = f

        btn = self.addButton("btnSave", "&Save")
        btn.top = - self.BUTTON_SPACE - btn.height
        btn.width = self.BUTTON_WIDTH
        btn.onClick = self.onSaveClick
        self.btnSave = btn

        btn = self.addButton("btnClose", "&Close")
        btn.top = - self.BUTTON_SPACE - btn.height
        btn.width = self.BUTTON_WIDTH
        btn.left = -self.BUTTON_SPACE - self.BUTTON_WIDTH
        btn.onClick = self.onCloseClick
        self.btnClose = btn

    def onSaveClick(self):
        """Set the token if it is valid.

        When Save is clicked the token is checked for valid formatting.
        It is then set in the database and the Namespace client is used to
        check whether there is a namespace associated with the token.

        If so, all is well.  Otherwise, the token is reset to its previous
        value and an error is displayed.

        :returns: None
        """
        token_value = self.token_field.getValue()
        current_token = self.token
        if "*" in token_value:
            _alert("There are * in the token value, which isn't valid. "
                   "Close the screen without saving if the token doesn't need "
                   "to be changed.")
            return

        if not self.UUID_REGEX.match(token_value):
            _alert("The provided token isn't a valid UUID. Please verify the "
                   "token format and try again.")
            return

        try:
            namespaces = NamespaceClient(token=token_value).list()
            if not namespaces:
                raise Exception("can't find a namespace with token {}.".format(
                    token_value))
            self.token = token_value
        except Exception as e:
            _alert("Failed to check the token wih the service.")
            _debug("Exception: {}".format(e))
            return

        try:
            set_token(token_value)
        except Exception as e:
            _alert("Failed to persist token in the database.")
            _debug("Exception: {}".format(e))
            return

        _alert("Token set!")
        _debug("token set to {} - namespace {}.".format(
                self.token[-6:], namespaces[0]["subdomain"]))

    def onCloseClick(self):
        """Close the UI if the Close button or window X are clicked."""
        self.closeUI()

