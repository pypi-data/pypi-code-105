"""
Tools for connecting to Adobe Sign.
"""
try:
    from accpac import *
except ImportError as e:
    pass

from datetime import datetime, timedelta
from pprint import pformat
import requests

from remote_actions import get_logger, AGREEMENTS_VIEW, TRANSIENT_DOCS_VIEW

logger = None

def log():
    global logger
    if not logger:
        logger = get_logger("adobe_sign")
    return logger

def add_workflow_agreement(wiid, agreement_id, signed, rejected, error):
    log().debug("Adding workflow agreement to DB {}/{}/{}/{}/{}".format(
        wiid, agreement_id, signed, rejected, error))

    agreements = openView(AGREEMENTS_VIEW)
    agreements.recordGenerate()
    agreements.put("AGREEID", agreement_id)
    agreements.put("WIID", wiid)
    agreements.put("SIGNEDSTEP", signed)
    agreements.put("REJECTSTEP", rejected)
    agreements.put("ERRORSTEP", error)
    agreements.put("STATUS", "IN PROGRESS")
    i = agreements.insert()
    agreements.close()
    if i != 0:
        log().error("Failed to add agreement to table: {}".format(i))
        return False
    return True

def add_agreement_docs(agreement_id, transient_document_ids):
    log().debug("Adding agreement {} docs {} to DB".format(
            agreement_id, transient_document_ids))
    tdocs = openView(TRANSIENT_DOCS_VIEW)
    results = []
    for tid in transient_document_ids:
        tdocs.recordGenerate()
        tid1 = tid[0:190]
        tid2 = tid[191:]
        tdocs.put("TDOCID1", tid1)
        tdocs.put("TDOCID2", tid2)
        tdocs.put("AGREEID", agreement_id)
        results.append(tdocs.insert())
    tdocs.close()
    if sum(results) == 0:
        return True
    log().error("Failed to insert documents: {}".format(results))
    return False

def delete_workflow_agreement(wiid):
    log().debug("Deleting workflow agreements for workflow {}".format(wiid))

    deleted_agreements = []

    agreements = openView(AGREEMENTS_VIEW)
    agreements.recordClear()
    agreements.order(1)
    br = agreements.browse("WIID = {}".format(wiid))
    if br == 0:
        while agreements.fetch() == 0:
            agree_id = agreements.get("AGREEID")
            if agreement.delete() != 0:
                log().debug("Failed to delete agreement {}".format(
                    agree_id))
            else:
                deleted_agreements.append(agree_id)
    agreements.close()

    log().debug("Deleting docs for agreements: {}".format(deleted_agreements))
    tdocs = openView(TRANSIENT_DOCS_VIEW)
    results = []
    tdocs.order(1)
    for agreeid in deleted_agreements:
        tdocs.recordClear()
        tdocs.browse("AGREEID = '{}'".format(agreeid))
        while tdocs.fetch() == 0:
            if tdocs.delete() != 0:
                log().error("Failed to delete transient docs for {}".format(
                    agreeid))
    tdocs.close()

    return True

def update_agreement_status(agreement_id, status):
    log().debug("Updating agreement {} status to {}.".format(
            agreement_id, status))
    agreements = openView(AGREEMENTS_VIEW)
    agreements.put("AGREEID", agreement_id)
    u = 1
    if agreements.read() == 0:
        agreements.put("STATUS", status)
        u = agreements.update()
    agreements.close()
    if u != 0:
        log().error("Failed to update agreement {} status to {}.".format(
            agreement_id, status))
        return False
    return True

def agreement_id_for_wiid(wiid):
    agreements = openView(AGREEMENTS_VIEW)
    agreements.order(1)
    agreements.browse("WIID = {}".format(wiid), 1)
    agreement_id = ""
    if agreements.fetch() == 0:
        agreement_id = agreements.get("AGREEID")
    agreements.close()
    if not agreement_id:
        log().error("failed to get agreement id for wiid {}.".format(wiid))
    return agreement_id


class AdobeSignClient():
    """The Adobe Sign Client connects and manages agreements over the API.

    :param view_name: the configuration view name.
    """
    REDIRECT_URI = "https://poplars.dev/adobe-sign-activate.html"
    BASE_URL = "https://secure.{shard}.adobesign.com"
    OAUTH_START_PATH = "/public/oauth"
    OAUTH_TOKEN_PATH = "/oauth/token"
    OAUTH_REFRESH_PATH = "/oauth/refresh"
    REST_ROOT = "/api/rest/v6"
    TRANSIENT_DOCS_PATH = "/transientDocuments"
    AGREEMENTS_PATH = "/agreements"
    AGREEMENT_PUBLIC_PATH = "/public/agreements/view/{agreement_id}"

    def __init__(self, view_name="REMOTEACTION.ADBSIGN"):
        self.view_name = view_name
        self.config = self.load_config()
        log().debug("Initialized new client:\n\n{}".format(self.config))
        if not self.config:
            raise RuntimeError("No Configuration Defined")

    def load_config(self):
        """Load the configuration from the database.

        :returns: configuration
        :rtype: dict
        """

        self._config = openView(self.view_name)
        if not self._config:
            return None

        self._config.recordClear()
        self._config.browse("", 1)
        if self._config.fetch() != 0:
            log().error("At least one config record must be defined.")
            return None

        return {
            "shard": self._config.get("SHARD"),
            "client_id": self._config.get("CLIENTID"),
            "client_secret": self._config.get("CLIENTSEC"),
            "access_point": self._config.get("ACCESSPT"),
            "code": self._config.get("CODE"),
            "access_token": self._config.get("ACCESSTK"),
            "refresh_token": self._config.get("REFRESHTK"),
            "expires_on": datetime.fromtimestamp(self._config.get("EXPIRESON")),
            }

    def write_config(self):
        """Write the configuration to the database.

        :returns: True on success else False
        :rtype: bool
        """
        log().debug("Writing config: {}".format(self.config))
        self._config.put("ACCESSTK", self.config.get("access_token", ""))
        self._config.put("REFRESHTK", self.config.get("refresh_token", ""))
        self._config.put("EXPIRESON", int(self.config.get("expires_on", datetime.now()).timestamp()))
        if self._config.update() != 0:
            errors = ErrorStack()
            output = [(errors.getPriority(i), errors.getText(i), )
                        for i in range(0, errors.count())]
            errors.clear()
            log().warning("Failed to write config: {}".format(
                    "\n".join(["{}: {}".format(o[0], o[1]) for o in output])))
            return False
        return True

    def setup_token(self):
        """Take the steps required to refresh or obtain a token.

        :returns: self.connected
        :rtype: bool
        """
        code = self.config.get('code')
        expires_on = self.config.get('expires_on')
        access_token = self.config.get('access_token')
        refresh_token = self.config.get('refresh_token')

        log().debug("Token setup starting for {} expiring on {}, access {}, "
                "refresh {}.".format(
                    code, expires_on, access_token[0:10], refresh_token[0:10]))

        if not code:
            log().debug("No code defined.")
            return False

        if access_token:
            if datetime.now() + timedelta(seconds=600) < expires_on:
                log().debug("Token valid. Connected.")
            else:
                log().debug("Token Expired. Refreshing.")
                self.refresh_token()
        else:
            log().debug("No access code. Obtaining tokens.")
            self.obtain_token()

        return self.connected

    @property
    def connected(self):
        """Connected if there is a valid access token in the configuration.

        :returns: True if connected else False
        :rtype: bool
        """
        return (self.config.get("access_token") and
                (datetime.now() + timedelta(seconds=600) < self.config.get(
                        'expires_on', 0)))

    def obtain_token(self):
        """Obtain new tokens for a Connection Code.

        :returns: True if tokens obtained else False
        :rtype: bool
        """

        params = {
            'grant_type': 'authorization_code',
            'code': self.config.get('code'),
            'client_id': self.config.get('client_id'),
            'client_secret': self.config.get('client_secret'),
            'redirect_uri': self.REDIRECT_URI,
        }
        response_json = {}
        log().debug("Obtaining new token set. Posting to {}. Params: {}".format(self.oauth_token_url, params))

        try:
            resp = requests.post(self.oauth_token_url, data=params)
            response_json = resp.json()
            if resp.status_code not in [200, 201]:
                raise RuntimeError("HTTP response {}".format(resp.status_code))
        except Exception as e:
            log().error("Failed to obtain new token: {}\n\n{}".format(
                    e, response_json))
            return False

        if 'access_token' in response_json:
            log().debug("New access token in response.")
            self.config['access_token'] = response_json.get('access_token')
            self.config['refresh_token'] = response_json.get('refresh_token')
            self.config['expires_on'] = datetime.now() + timedelta(
                    seconds=response_json.get('expires_in'))
            self.write_config()
        else:
            log().error("No access token in response: {}/{}/{}".format(
                    resp.status_code, resp.text, response_json))

        return True

    def refresh_token(self):
        """Refresh an expired token.

        :returns: True if tokens obtained else False
        :rtype: bool
        """
        params = {
            'grant_type': 'refresh_token',
            'client_id': self.config.get('client_id'),
            'client_secret': self.config.get('client_secret'),
            'refresh_token': self.config.get('refresh_token'),
        }
        response_json = {}
        try:
            resp = requests.post(self.oauth_refresh_url, data=params)
            response_json = resp.json()
            if resp.status_code not in [200, 201]:
                raise RuntimeError("HTTP response {}".format(resp.status_code))
        except Exception as e:
            log().error("Failed to refersh token: {}\n\n{}".format(
                    e, response_json))
            return False

        if 'access_token' in response_json:
            self.config['access_token'] = response_json.get('access_token')
            self.config['expires_on'] = datetime.now() + timedelta(
                    seconds=response_json.get('expires_in'))
            self.write_config()

        return True

    @property
    def base_url(self):
        return self.BASE_URL.format(shard=self.config.get('shard'))

    @property
    def oauth_start_url(self):
        return self.base_url + self.OAUTH_START_PATH

    @property
    def oauth_token_url(self):
        return self.base_url + self.OAUTH_TOKEN_PATH

    @property
    def oauth_refresh_url(self):
        return self.base_url + self.OAUTH_REFRESH_PATH

    @property
    def transient_documents_url(self):
        return self.config.get("access_point", "") + self.REST_ROOT + self.TRANSIENT_DOCS_PATH

    @property
    def agreements_url(self):
        return self.config.get("access_point", "") + self.REST_ROOT + self.AGREEMENTS_PATH

    def agreement_url(self, agreement_id):
        return self.agreements_url + "/{}".format(agreement_id)

    def agreement_combined_document_url(self, agreement_id):
        return self.agreement_url(agreement_id) + "/combinedDocument"

    def agreement_audit_report_url(self, agreement_id):
        return self.agreement_url(agreement_id) + "/auditTrail"

    def agreement_events_url(self, agreement_id):
        return self.agreement_url(agreement_id) + "/events"

    def agreement_public_url(self, agreement_id):
        return self.base_url + self.AGREEMENT_PUBLIC_PATH.format(
                agreement_id=agreement_id)

    @property
    def headers(self):
        return { 'Authorization': 'Bearer {}'.format(
                self.config.get("access_token", "")) }

    def upload_document(self, document_path):
        """Upload a document to Adobe Sign.

        :param document_path: path of the PDF document to upload.
        :type document_path: pathlib.Path
        :returns: Transient Document ID on success else ""
        :rtype: str
        """
        log().debug("Uploading {}".format(document_path))
        if document_path.exists():
            try:
                headers = self.headers
                data = { 'File-Name': document_path.name, 'Mime-Type': 'application/pdf' }
                files = { 'File': document_path.open('rb') }
                resp = requests.post(self.transient_documents_url,
                                     headers=self.headers,
                                     data=data,
                                     files=files)
                response_json = resp.json()
                if resp.status_code not in [200, 201]:
                    raise RuntimeError("HTTP response {}".format(resp.status_code))
            except Exception as e:
                log().error("Failed to upload document: {}\n\n{}".format(
                        e, response_json))
                return ""
        log().debug("Created document with id {}".format(
                response_json.get("transientDocumentId")))

        return response_json.get("transientDocumentId")

    def create_agreement(self, name, transient_document_ids, signer_emails,
                         **kwargs):
        """Create a new agreement.

        kwargs will be merged with the API create payload.

        :param name: Name and title of the agreement.
        :type name: str
        :param transient_document_ids: a list of transient document ids that
            make up the agreement.
        :type transient_document_ids: str[]
        :param signer_emails: email addresses for signers.
        :type signer_emails: str[]
        :returns: Agreement ID on success else ""
        :rtype: str
        """
        file_infos = [{"transientDocumentId": id}
                      for id in transient_document_ids]
        member_infos = [{"email": email} for email in signer_emails]

        participant_sets_infos = [{
            "memberInfos": [mi, ],
            "order": i + 1,
            "role": "SIGNER" } for i, mi in enumerate(member_infos)]

        payload = {
            "fileInfos": file_infos,
            "name": name,
            "participantSetsInfo": participant_sets_infos,
            "signatureType": "ESIGN",
            "state": "IN_PROCESS"
        }

        # Merge - do not overwrite.
        for arg, val in kwargs.items():
            if arg not in payload:
                payload[arg] = val

        log().debug("agreement create payload: \n{}".format(
                pformat(payload)))

        response_json = {}
        try:
            resp = requests.post(self.agreements_url,
                                 headers=self.headers,
                                 json=payload)
            response_json = resp.json()
            if resp.status_code not in [200, 201]:
                raise RuntimeError("HTTP response {}".format(resp.status_code))
        except Exception as e:
            log().error("Failed to create agreement: {}\n\n{}".format(
                    e, response_json))
            return ""

        log().debug("Created agreement with id {}".format(
                response_json.get("id")))

        return response_json.get("id")

    def agreement_details(self, agreement_id):
        """Get the details of an agreement.

        :param agreement_id: the ID of the agreement to get.
        :type agreement_id: str
        :returns: agreement details or {}
        :rtype: dict
        """
        response_json = {}
        try:
            resp = requests.get(self.agreement_url(agreement_id),
                                 headers=self.headers)
            response_json = resp.json()
            if resp.status_code != 200:
                raise RuntimeError("HTTP response {}".format(resp.status_code))
        except Exception as e:
            log().error("Failed to get agreement details: {}\n\n{}".format(
                    e, response_json))
            return {}
        return response_json

    def download_agreement_document(self, agreement_id):
        """Download the combined documents and return the PDF content.

        :param agreement_id: the ID of the agreement to get docs for.
        :type agreement_id: str
        :returns: pdf content
        :rtype: bytes
        """
        try:
            resp = requests.get(
                    self.agreement_combined_document_url(agreement_id),
                    headers=self.headers)
            if resp.status_code != 200:
                raise RuntimeError("HTTP response {}".format(resp.status_code))
        except Exception as e:
            log().error("Failed to get signed document: {}\n\n{}".format(
                    e, resp.content))
            return False
        log().debug("downloaded agreement {} len {} bytes".format(
                agreement_id, len(resp.content)))
        return resp.content

    def download_agreement_audit_report(self, agreement_id):
        """Download the audit report and return the PDF content.

        :param agreement_id: the ID of the agreement to get docs for.
        :type agreement_id: str
        :returns: pdf content
        :rtype: bytes
        """
        try:
            resp = requests.get(
                    self.agreement_audit_report_url(agreement_id),
                    headers=self.headers)
            if resp.status_code != 200:
                raise RuntimeError("HTTP response {}".format(resp.status_code))
        except Exception as e:
            log().error("Failed to get audit report document: {}\n\n{}".format(
                    e, resp.content))
            return False
        log().debug("downloaded audit report {} len {} bytes".format(
                agreement_id, len(resp.content)))
        return resp.content

    def agreement_events(self, agreement_id):
        """Download the event stream for an agreement.

        :param agreement_id: the ID of the agreement to get events for.
        :type agreement_id: str
        :returns: json event steam
        :rtype: dict
        """
        response_json = {}
        try:
            resp = requests.get(self.agreement_events_url(agreement_id),
                                 headers=self.headers)
            response_json = resp.json()
            if resp.status_code != 200:
                raise RuntimeError("HTTP response {}".format(resp.status_code))
        except Exception as e:
            log().error("Failed to get agreement events: {}\n\n{}".format(
                    e, response_json))
            return False
        return response_json.get('events', {})
