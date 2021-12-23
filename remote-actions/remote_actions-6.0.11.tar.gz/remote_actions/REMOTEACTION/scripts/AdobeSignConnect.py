""" The Remote Actions Adobe Sign Connect UI walks you through
the process of connecting the Adobe Sign Service.
"""
import sys
import datetime
import traceback
import subprocess
import webbrowser

try:
    from accpac import *
    from remote_actions import get_token, get_logger, debug_enabled, ADMIN_USER
    from remote_actions.services.adobe_sign import AdobeSignClient
except ImportError:
    pass


DEBUG = False
NAME = "Adobe Sign Connect"
VERSION = '6.0.11'
logger = None
AUTHORIZE_URL = ("https://secure.{shard}.adobesign.com/public/oauth?"
                 "redirect_uri=https://poplars.dev/adobe-sign-activate.html&"
                 "response_type=code&client_id={client_id}&"
                 "scope=user_read+agreement_read+agreement_write+agreement_send")

## Entry point

def main(args):
    global logger
    global DEBUG
    DEBUG = debug_enabled()
    logger = get_logger("adobe_sign_connect")
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
CONFIG = {
            "shard": '',
            "client_id": '',
            "client_secret": '',
            "access_point": '',
            "code": '',
            "access_token": '',
            "refresh_token": '',
            "expires_on": 0,
            }

class RemoteActionsUI(UI):
    """UI for Adobe Sign Connect.

    This UI walks users through the process of connecting to Adobe Sign
    using OAuth.
    """

    # Custom control constants
    BUTTON_WIDTH = 1265
    BUTTON_SPACE = 150

    def __init__(self):
        UI.__init__(self)
        shown = False
        self.title = "Remote Actions - Connect to Adobe Sign"
        self.client = None
        try:
            if self.setup_client():
                self.client.setup_token()
            self.createScreen()
            self.set_controls_for_state()
        except Exception as e:
            if not shown:
                self.show()
            _alert("Error starting up: {}".format(
                e))
            _debug(e, excinfo=sys.exc_info()[2])
            self.closeUI()
        else:
            self.onClose = self.onCloseClick
        logger.info("AdobeSignConnect version {} started.".format(VERSION))

    def setup_client(self):
        """Setup the Adobe Sign Client.

        This can fail if there is no configuration yet. If that is
        the case, use a placeholder config until we have enough information
        to create the client.
        """
        try:
            self.client = AdobeSignClient()
            self.config = self.client.config
        except RuntimeError as e:
            self.config = CONFIG

        return self.client

    def values_to_config(self):
        """Copy the values from the interface into the configuration.

        Capture user input in a config dictionary that mirrors the client
        config dictionary.
        """
        self.config["client_id"] = self.client_id
        self.config["client_secret"] = self.client_secret
        self.config["shard"] = self.shard
        self.config["code"] = self.connection_code

        return self.config

    @property
    def shard(self):
        """Get the value from the Shard Input Field."""
        return self.shard_input.getValue().strip()

    @property
    def client_id(self):
        """Get the value from the Client ID Input Field."""
        return self.client_id_input.getValue().strip()

    @property
    def access_point(self):
        """Get the value from the Access Point Input Field."""
        return self.access_point_input.getValue().strip().rstrip('/')

    @property
    def connection_code(self):
        """Get the value from the Connection Code Input Field."""
        return self.connection_code_input.getValue().strip()

    @property
    def client_secret(self):
        """Get the value from the Client Secret Input Field."""
        return self.client_secret_input.getValue().strip()

    def set_status(self, status):
        """Set the Status Label."""
        self.status_label.setText("Status: {}".format(status))

    def set_controls_for_state(self):
        """Set the control states based on the state of the configuration."""
        # Disable everything
        self.shard_input.disable()
        self.client_id_input.disable()
        self.client_secret_input.disable()
        self.access_point_input.disable()
        self.connection_code_input.disable()
        self.authorize_button.disable()
        self.connect_button.disable()

        if self.client and self.client.connected:
            self.set_status("Connected")
            return

        if not self.shard:
            self.shard_input.enable()
            return

        self.set_status("Partially Configured")

        self.client_id_input.enable()
        if not self.client_id:
            return

        self.client_secret_input.enable()
        if not self.client_secret:
            return

        self.set_status("Ready to Authorize")
        self.authorize_button.enable()

        self.access_point_input.enable()
        if not self.access_point:
            return

        self.connection_code_input.enable()
        if not self.connection_code:
            return
        self.set_status("Ready to Connect")

        self.connect_button.enable()

    def createScreen(self):
        """Configure and render the fields and buttons."""
        top = 150
        f = self.addLabel("statusLabel")
        f.width = 5000
        f.setText("Status: Not Configured")
        f.top = top
        self.status_label = f

        top += 350
        f = self.addUIField("shardInput")
        f.controlType = "EDIT"
        f.size = 250
        f.top = top
        f.width = 5000
        f.labelWidth = 60
        f.caption = "Shard"
        f.hasFinder = False
        f.setValue(self.config["shard"])
        f.enabled = True
        f.onChange = self.getOnFieldChangedCallback('shard')
        self.shard_input = f

        top += 350
        f = self.addUIField("clientIdInput")
        f.controlType = "EDIT"
        f.size = 250
        f.top = top
        f.width = 5000
        f.labelWidth = 60
        f.caption = "Client ID"
        f.hasFinder = False
        f.setValue(self.config["client_id"])
        f.enabled = True
        f.onChange = self.getOnFieldChangedCallback('client_id')
        self.client_id_input = f

        top += 350
        f = self.addUIField("clientSecretInput")
        f.controlType = "EDIT"
        f.size = 250
        f.top = top
        f.width = 5000
        f.labelWidth = 60
        f.caption = "Client Secret"
        f.hasFinder = False
        f.setValue(str(self.config['client_secret']))
        f.enabled = False
        f.onChange = self.getOnFieldChangedCallback('client_secret')
        self.client_secret_input = f

        top += 350
        btn = self.addButton("btnAuthorize", "&Authorize")
        btn.top = - self.BUTTON_SPACE - btn.height
        btn.width = self.BUTTON_WIDTH
        btn.left = 2500
        btn.onClick = self.onAuthorizeClick
        btn.top = top
        self.authorize_button = btn

        top += 350
        f = self.addUIField("accessPointInput")
        f.controlType = "EDIT"
        f.size = 250
        f.width = 5000
        f.labelWidth = 60
        f.caption = "Access Point"
        f.hasFinder = False
        f.setValue(str(self.config['access_point']))
        f.enabled = False
        f.top = top
        f.onChange = self.getOnFieldChangedCallback('access_point')
        self.access_point_input = f

        top += 350
        f = self.addUIField("connectionCodeInput")
        f.controlType = "EDIT"
        f.size = 250
        f.width = 5000
        f.labelWidth = 60
        f.caption = "Connection Code"
        f.hasFinder = False
        f.setValue(str(self.config['code']))
        f.enabled = False
        f.top = top
        f.onChange = self.getOnFieldChangedCallback('code')
        self.connection_code_input = f

        btn = self.addButton("btnConnect", "Co&nnect")
        btn.top = - self.BUTTON_SPACE - btn.height
        btn.width = self.BUTTON_WIDTH
        btn.left = -self.BUTTON_SPACE - (2*self.BUTTON_WIDTH)
        btn.onClick = self.onConnectClick
        btn.top =  - self.BUTTON_SPACE - btn.height
        self.connect_button = btn

        btn = self.addButton("btnClose", "&Close")
        btn.top = - self.BUTTON_SPACE - btn.height
        btn.width = self.BUTTON_WIDTH
        btn.left = -self.BUTTON_SPACE - self.BUTTON_WIDTH
        btn.onClick = self.onCloseClick
        self.btnClose = btn

        self.show()

    def getOnFieldChangedCallback(self, config_field):
        """Get an onchange callback that writes a field to the config.

        :param config_field: the field in the config to update.
        """
        def onFieldChanged(old, new):
            if new:
                logger.info("Setting config.{} from '{}' to '{}'".format(
                        config_field, old, new))
                self.config[config_field] = new
                self.set_controls_for_state()
        return onFieldChanged

    def persist_config(self):
        """Write the current config to the DB."""
        v = openView("REMOTEACTION.ADBSIGN")
        v.recordClear()
        v.put("SHARD", self.shard)
        if v.read() != 0:
            v.recordGenerate()
            v.put("SHARD", self.shard)
            v.put("CLIENTID", self.client_id)
            v.put("CLIENTSEC", self.client_secret)
            v.put("ACCESSPT", self.access_point)
            v.put("CODE", self.connection_code)
            v.insert()
        else:
            v.put("CLIENTID", self.client_id)
            v.put("CLIENTSEC", self.client_secret)
            v.put("ACCESSPT", self.access_point)
            v.put("CODE", self.connection_code)
            v.update()
        v.close()

    def onAuthorizeClick(self):
        """Open a webbrowser so the suer can authorize the application."""
        auth_url = AUTHORIZE_URL.format(
                shard=self.shard, client_id=self.client_id)
        logger.info("Authorizing API application from URL {}".format(auth_url))
        webbrowser.open_new(auth_url)

    def onConnectClick(self):
        """Connect and obtain tokens."""
        self.persist_config()
        self.setup_client()

        logger.info("Connect clicked.")

        if not self.client:
            _alert("Client isn't setup, cannot connect.")

        self.client.config = self.config

        logger.info("Connect clicked with config {}".format(self.config))

        if self.client.setup_token():
            self.set_status("connected.")
            logger.info("Connect succeeded - expires on {}".format(
                    self.client.config.get("expires_on")))
        else:
            _alert("Failed to obtain token. Try re-authorizing and "
                   "obtaining a new Connection Code.\n\n"
                   "More details are available in the log.")

        self.set_controls_for_state()

    def onCloseClick(self):
        """Close the UI if the Close button or window X are clicked."""
        self.closeUI()

