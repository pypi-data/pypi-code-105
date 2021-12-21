"""
Functions and classes for device registration with Azure IoT Central
"""
from ntpath import join
import os
import subprocess
import json
import shutil
from logging import getLogger
from datetime import datetime
from requests import Session, status_codes
from requests import codes
from pykitinfo import pykitinfo
from pytrustplatform.cert_get_data import cert_get_common_name_from_pem
from .status_codes import STATUS_SUCCESS, STATUS_FAILURE
from .pyazureutils_errors import ApplicationError, RestApiError
from .pyazureutils_errors import AzureConnectionError, KitConnectionError, DeviceTemplateError

def iotcentral_register_device(app_name=None, certificate_file=None, display_name=None, subscription=None,
                               device_template=None):
    """
    Register an IoT device in Azure's IoTCentral

    Registration requires that the user logs into Azure using the Azure CLI "az"
    Tokens will be collected from the user's Azure local token storage

    Registration uses an application name which is either:

    - collected from IoTCentral account (first one found is used)
    - passed in as an argument

    Registration uses a certificate which is either:

    - collected from local certificate storage for a kit, if a kit has been provisioned using this machine
    - passed in as a filename argument

    Registration uses a device name which is derived from the subject common name of the certificate used

    Registration uses a display name which is either:

    - derived from the kit serial number (if a kit is connected)
    - passed in as an argument

    :param app_name: Application Name to register device with
    :param certificate_file: Device certificate PEM file
    :param display_name: Display name to register device with
    :param device_template: Device template to use for registration
    """
    logger = getLogger(__name__)

    # Start a session communicating with IoTCentral
    azuresession = AzureIotCentralSession(subscription=subscription)
    try:
        azuresession.connect()
    except Exception as err:
        raise(AzureConnectionError("Unable to connect to Azure"))

    # Start session
    az = AzureIotCentral(azuresession, app_name)

    # Check and report subscriptions
    logger.info("\nSubscription:")
    subscriptions = az.get_subscriptions()
    logger.info("%d subscriptions(s) found for this tenant", len(subscriptions))

    # List available subscriptions
    valid_subscriptions = []
    for sub in subscriptions:
        valid_subscriptions.append(sub['displayName'])

    if subscription:
        logger.info("Connected to Azure IoTCentral subscription '%s'", subscription)
    else:
        logger.info("Connected to Azure IoTCentral using default subscription...")
        logger.info("You can specify an alternative subscription using the 'subscription' argument to this CLI.")
        logger.info("You can change your default subscription using az CLI: 'az account set --subscription <name>'")
        logger.info("Available subscriptions:")
        for sub in valid_subscriptions:
            logger.info("- '%s'", sub)

    # Check application
    logger.info("\nApplication:")
    apps = az.list_applications()
    logger.info("%d application(s) found on subscription", len(apps))

    # List of app names
    valid_apps = []
    for app in apps:
        valid_apps.append(app['name'])
        logger.info("- %s ('%s')", app['name'], app['displayName'])

    # Check that there are applications available
    if not apps:
        if not subscription:
            subscription = 'default - not specified'
        msg = "No applications found - have you selected the correct subscription ({})?".format(subscription)
        raise ApplicationError(msg)

    # If the application name is not specified, we can only proceed if there is one
    if not app_name:
        if len(apps) == 1:
            app_name = apps[0]['name']
            display_name = apps[0]['displayName']
            logger.warning("Application not specified - continuing using application '%s'", app_name)
        else:
            msg = "Application name not specified - it must be one of: {}".format(",".join(valid_apps))
            raise ApplicationError(msg)
    else:
        # If the application name is specified, it must be valid...
        # But in 'free trials' it is possible that the app is not listed, so warn and continue
        if not app_name in valid_apps:
            logger.warning("Application '%s' not listed on subscription (continuing with registration)", app_name)

    logger.info("Using application: %s", app_name)
    az.set_app_name(app_name)

    # Certificate is taken from a local cert storage, which contains certificates for kits which have been provisioned;
    # or passed in as an argument
    logger.info("\nCertificate:")
    if certificate_file:
        cert_file_name = certificate_file
        logger.info("Using certificate file '%s'", cert_file_name)

        # Try to open the certificate file.  Will raise exception if not found
        with open(cert_file_name, "r") as cert_file:
            certificate = cert_file.read()
    else:
        # Look for connected kits
        kits = pykitinfo.detect_all_kits()
        if not kits:
            raise KitConnectionError("No kit found. Either connect a kit or provide a certificate as an argument.")
        if len(kits) > 1:
            logger.error("Too many kits found - specify serial number:")
            for kit in kits:
                logger.error("%s: %s", kit['debugger']['kitname'], kit['usb']['serial_number'])
            raise KitConnectionError("Too many kits connected!")

        serialnumber = kits[0]['usb']['serial_number']
        kitname = kits[0]['debugger']['kitname']
        logger.info("Using kit '%s (%s)'", kitname, serialnumber)

        # Check in local folder
        certs_dir = os.path.join(os.path.expanduser("~"), ".microchip-iot", serialnumber)
        cert_file_name = os.path.abspath(os.path.join(certs_dir, "device.crt"))
        logger.info("Using certificate file '%s'", cert_file_name)

        try:
            # Try to open the certificate file
            with open(cert_file_name, "r") as cert_file:
                certificate = cert_file.read()
        except FileNotFoundError:
            logger.error("Unable to load certificate from file: '%s' - has the kit been provisioned?", cert_file_name)
            raise

    logger.info("Certificate loaded")

    # Extract from certificate
    logger.info("Extracting common name from certificate (to use as device ID")
    device_id = cert_get_common_name_from_pem(certificate)
    logger.info("Device ID will be: '%s'", device_id)

    # Retrieve device templates from the server
    logger.info("\nTemplate:")
    templates = az.get_device_templates()
    logger.info("%d templates(s) found for this application", len(templates))

    # No templates found?
    if not templates:
        msg = "No templates found for application '{}'".format(app_name)
        if "PIC-IoT" in kitname:
            logger.error("When using PIC-IoT boards, the 'PIC_IoT WM' device template should be used.")
            logger.error("This is available at https://github.com/Azure-Samples/Microchip-PIC-IoT-Wx/blob/main/device_model/pic_iot_wm-1.json")
        logger.error("Store the device template to your application using the Azure Portal")
        raise DeviceTemplateError(msg)

    # List templates
    valid_templates = []
    for template in templates:
        id = template['@id']
        displayname = template['displayName']
        logger.info("- %s (%s)", displayname, id)
        valid_templates.append({'id': id, 'displayname': displayname})

    # If there is only one, use it (and notify)
    if len (valid_templates) == 1 and not device_template:
        device_template = valid_templates[0]['displayname']
        logger.warning("Device template not specified - using '%s'", device_template)

    # If there are several device templates available, it must be specified by the user
    if len (valid_templates) > 1 and not device_template:
        msg = "Device template not specified -  it must be one of: {}".format(",".join([i['displayname'] for i in valid_templates]))
        raise DeviceTemplateError(msg)

    # If the device template name is specified, it must be available on iotcentral
    if device_template and not device_template in [i['displayname'] for i in valid_templates]:
        msg = "Specified device template '{}' not found - it must be one of: {}".format(
            device_template, ",".join([i['displayname'] for i in valid_templates]))
        raise DeviceTemplateError(msg)

    # Map device template display name to template ID
    template_device_id = None
    for i in valid_templates:
        if i['displayname'] == device_template:
            template_device_id = i['id']
            break

    if not template_device_id:
        raise DeviceTemplateError("Unable to find device template ID")

    logger.info("\nRegistration:")
    logger.info("Using device template: %s (%s)", device_template, template_device_id)

    # Now create the device
    logger.info("Creating device '%s' from template '%s'", device_id, template_device_id)
    az.create_device(device_id, template_device_id, display_name)

    # Check by read-back
    logger.info("Checking device")
    az.get_device(device_id)

    # Do device attestation
    logger.info("Creating device attestation using certificate")
    az.create_device_attestation(device_id, certificate)

    # Check by readback
    logger.info("Checking device attestation")
    az.get_device_attestation(device_id)

    # Done
    logger.info("Registration complete!")
    return STATUS_SUCCESS

class AzureIotCentralSession:
    """
    Session handling for Azure IoT Central
    """
    def __init__(self, subscription=None):
        self.logger = getLogger(__name__)
        self.management_headers = None
        self.apps_headers = None
        self.management_session = None
        self.apps_session = None
        self.params = None
        self.management_token = None
        self.iotcentral_app_token = None
        self.subscription = subscription
        self.az_cmd = shutil.which("az")
        if not self.az_cmd:
            raise Exception("Azure CLI (az) not found.")
        self.logger.debug("Found Azure CLI: %s", self.az_cmd)

    def connect(self):
        """Connect to Azure services by creating access tokens.

        :raises Exception: If no access tokens could be created.
        """
        if not self.management_token or not self._is_token_valid(self.management_token):
            self.login_info = json.loads(self._az_login())
        self.management_token = self._az_get_resource_management_token(self.subscription)
        self.iotcentral_app_token = self._az_get_iotcentral_app_access_token()

        if not self.iotcentral_app_token or not self.management_token:
            raise Exception("Apps token could not be retrieved")

        self.apps_session = Session()
        self.params = {"api-version":"1.0"}
        self.management_headers = {"Authorization": "Bearer {}".format(self.management_token['accessToken'])}
        self.apps_headers = {"Authorization": "Bearer {}".format(self.iotcentral_app_token['accessToken'])}

    def _is_token_valid(self, auth_token):
        """ Check if a local token is valid """
        if datetime.utcnow() > datetime.strptime(auth_token['expiresOn'], '%Y-%m-%d %H:%M:%S.%f'):
            return False
        return True

    def _az_get_resource_management_token(self, subscription=None):
        """
        Retrieve access tokens from Azure account using CLI

        :param subscription: subscription to use
        :type subscription: str, optional
        """
        cmd = [self.az_cmd, "account", "get-access-token"]
        if subscription:
            cmd += ["--subscription", f"{subscription}"]
        process = subprocess.run(cmd, shell=False, stdout=subprocess.PIPE, universal_newlines=True, check=True)
        if process.returncode:
            self.logger.error("Unable to run Azure CLI")
            self.logger.debug("Stdout returned: %s", process.stdout)
            raise Exception("AZ CLI not installed, or inaccessible!")
        token = json.loads(process.stdout)
        self.logger.debug("Azure resource management token collected:")
        self.logger.debug("Type: %s", token['tokenType'])
        self.logger.debug("Tenant: %s", token['tenant'])
        self.logger.debug("Subscription: %s", token['subscription'])
        self.logger.debug("Expires: %s", token['expiresOn'])
        return token

    def _az_get_iotcentral_app_access_token(self):
        """ Retrieve iotcentral app access token from Azure account using CLI """
        process = subprocess.run([self.az_cmd, "account", "get-access-token", "--resource",
                                  "https://apps.azureiotcentral.com"],
                                 shell=False, stdout=subprocess.PIPE, universal_newlines=True, check=True)
        if process.returncode:
            self.logger.error("Unable to run Azure CLI")
            self.logger.debug("Stdout returned: %s", process.stdout)
            raise Exception("AZ CLI not installed, or inaccessible!")

        token = json.loads(process.stdout)
        self.logger.debug("Apps token collected:")
        self.logger.debug("Type: %s", token['tokenType'])
        self.logger.debug("Tenant: %s", token['tenant'])
        self.logger.debug("Subscription: %s", token['subscription'])
        self.logger.debug("Expires: %s", token['expiresOn'])
        return token

    def _check_all_token_validity(self, tokens):
        """ Filter tokens by validity """
        valid_tokens = []
        for token in tokens:
            if self._is_token_valid(token):
                valid_tokens.append(token)
            else:
                self.logger.debug("Expired token")

        return valid_tokens

    def _az_login(self):
        """ Login to Azure using CLI """
        self.logger.info("Logging in using 'az login'")
        process = subprocess.run([self.az_cmd, "login"], stdout=subprocess.PIPE, shell=False, check=True)
        if process.returncode:
            self.logger.error("Unable to run Azure CLI")
            raise Exception("AZ CLI not installed, or inaccessible!")
        return process.stdout

    def az_cli_command(self, command):
        """ Execute an Azure CLI command """
        cmd = command.split(' ')
        # add absolute path for az command instead
        cmd[0] = self.az_cmd
        process = subprocess.run(cmd, shell=False, stdout=subprocess.PIPE,
                                 universal_newlines=True, check=True)
        if process.returncode:
            self.logger.error("Unable to run Azure CLI")
            raise Exception("AZ CLI not installed, or inaccessible!")
        return process.stdout

    def az_rest_get(self, url):
        """ Make a rest-api GET call to Azure IoTCentral"""
        if "api-version" in url:
            params = {}
        else:
            params = self.params

        if "management.azure" in url:
            return self.apps_session.get(url=url, headers=self.management_headers, params=params).json()
        return self.apps_session.get(url=url, headers=self.apps_headers, params=params).json()

    def az_rest_put(self, url, json_content=None):
        """ Make a rest-api PUT call to Azure IoTCentral"""
        if "api-version" in url:
            params = {}
        else:
            params = self.params

        if "management.azure" in url:
            return self.apps_session.put(url=url, headers=self.management_headers, params=params, json=json_content).json()
        return self.apps_session.put(url=url, headers=self.apps_headers, params=params, json=json_content).json()


class AzureIotCentral:
    """
    Wrapper for interaction with Azure IoT Central
    """
    def __init__(self, session, app_name):
        self.logger = getLogger(__name__)
        self.session = session
        self.app_name = app_name

    def set_app_name(self, app_name):
        """ Set the app name """
        self.app_name = app_name

    # az commands using subprocess
    def list_applications(self):
        """ List applications using AZ CLI """
        self.logger.info("Retrieving application list...")
        cmd = 'az iot central app list'
        apps = self.session.az_cli_command(cmd)
        return json.loads(apps)

    # Rest-API calls
    def _check_rest_error_get(self, response):
        """Checks for success of a GET call"""
        if 'error' in response.keys():
            raise RestApiError(msg=response['error']['message'], code=response['error']['code'])
        return response

    def _check_rest_error_put(self, response):
        """Checks for success of a PUT call"""
        if 'error' in response.keys():
            raise RestApiError(msg=response['error']['message'], code=response['error']['code'])
        return response

    def get_subscriptions(self):
        """ Retrieve subscriptions via REST API call """
        self.logger.info("Retrieving subscription list...")
        result = self.session.az_rest_get("https://management.azure.com/subscriptions?api-version=2021-04-01")
        return self._check_rest_error_get(result)['value']

    def get_device_templates(self):
        """ Retrieve device templates via REST API call """
        self.logger.info("Retrieving device templates...")
        url = "https://{}.azureiotcentral.com/api/deviceTemplates".format(self.app_name)
        result = self.session.az_rest_get(url)
        return self._check_rest_error_get(result)['value']

    def get_device_template(self, template_id):
        """
        Get a device template by ID via REST API call.

        :param template_id: Template ID as defined by the DTDL e.g. dtmi:com:Microchip:PIC_IoT_WM;1 for the
            PIC-IoT Wx. More info
            `here <https://github.com/Azure/opendigitaltwins-dtdl/blob/master/DTDL/v2/dtdlv2.md#digital-twin-model-identifier>`_
        :type template_id: str
        :return: result of the REST request
        :rtype: str
        """
        self.logger.info("Retrieving device template for %s...", template_id)
        url = f"https://{self.app_name}.azureiotcentral.com/api/deviceTemplates/{template_id}"
        result = self.session.az_rest_get(url)
        return self._check_rest_error_get(result)

    def create_device(self, device_id, template, display_name=None):
        """
        Create device via REST API call

        :param device_id: IoT central device ID
        :type device_id: str
        :param template: template to use for creation
        :type template: str
        :param display_name: friendly name to use
        :type display_name: optional, str
        """
        url = "https://{}.azureiotcentral.com/api/devices/{}".format(self.app_name, device_id)
        if not display_name:
            display_name = device_id
        device = {
            'displayName': display_name,
            'simulated': False,
            'template': template
        }
        result = self.session.az_rest_put(url, json_content=device)
        return self._check_rest_error_put(result)

    def get_device(self, device_id):
        """
        Retrieve device info via REST API call

        :param device_id: IoT central device ID
        :type device_id: str
        """
        url = "https://{}.azureiotcentral.com/api/devices/{}?".format(self.app_name, device_id)
        result = self.session.az_rest_get(url)
        return self._check_rest_error_get(result)

    def get_device_attestation(self, device_id):
        """
        Retrieve device attestation via REST API call

        :param device_id: IoT central device ID
        :type device_id: str
        """
        url = "https://{}.azureiotcentral.com/api/devices/{}/attestation".format(self.app_name, device_id)
        result = self.session.az_rest_get(url)
        return self._check_rest_error_get(result)

    def create_device_attestation(self, device_id, certificate):
        """
        Create device attestation via REST API call

        :param device_id: IoT central device ID
        :type device_id: str
        :param certificate: certificate for enrollment
        :type certificate: str
        """
        url = "https://{}.azureiotcentral.com/api/devices/{}/attestation".format(self.app_name, device_id)
        attestation = {
            "type": "x509",
            "x509": {
                "clientCertificates": {
                    "primary": {
                        "certificate": certificate
                    }
                }
            }
        }
        return self.session.az_rest_put(url, json_content=attestation)
