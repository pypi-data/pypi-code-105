"""
The Remote Actions Fleeting Form Client creates, reads, and applies
fleeting forms to workflows.
"""
try:
    from accpac import *
except ImportError:
    pass

from datetime import datetime, timedelta
from pathlib import Path
import requests

from remote_actions import get_token

def create_form(type_, wiid, form_controls,
                title, content, actions, **initials):
    """Create a form.

    Any arguments passed in the keyword arguments (``initials``) will
    be treated as initial values for fields of that name.

    For example, if a form contained a field name ``APPROVALCOMMENT``,
    it can be defaulted to "Comments are required" by using the following
    call to create_form::

        create_form(wiid, title, content,
                    APPROVALCOMMENT="Comments are required.")

    :param type_: the form type, determines the handler used by the poller.
    :type type_: str
    :param wiid: workflow instance ID
    :type wiid: int
    :param form_controls: list of control definitions for the form.
    :type form_controls: dict
    :param title: the title to display above the form
    :type title: str
    :param content: the instructions to display above the form.
    :type content: str
    :param actions: a map of button labels to next steps.
    :type actions: { label: stepname, label2: stepname2, ...}
    :param initials: key value pairs of initial field values.
    :type initials: ``str=object``
    :returns: form dictionary
    :rtype: dict
    :raises Exception: on API create failure.
    """

    app =   {
                'wiid': wiid,
                'steps': actions,
                'type': type_,
                'org': org,
            }

    template = {
        'title': title,
        'content': content,
        'actions':  [{'label': a} for a in actions.keys()],
        'form_controls': form_controls,
    }

    for field in template['form_controls']:
        if field['name'] in initials:
            field['initial'] = initials[field['name']]

    return FormClient().create(template=template, app=app)


def create_workflow_approval_form(wiid, form_controls, title, content,
                                  actions, **initials):
    """Create a workflow approval form.

    Any arguments passed in the keyword arguments (``initials``) will
    be treated as initial values for fields of that name.

    For example, if a form contained a field name ``APPROVALCOMMENT``,
    it can be defaulted to "Comments are required" by using the following
    call to create_form::

        create_form(wiid, title, content,
                    APPROVALCOMMENT="Comments are required.")

    :param wiid: workflow instance ID
    :type wiid: int
    :param form_controls: list of control definitions for the form.
    :type form_controls: dict
    :param title: the title to display above the form
    :type title: str
    :param content: the instructions to display above the form.
    :type content: str
    :param actions: a map of button labels to next steps.
    :type actions: { label: stepname, label2: stepname2, ...}
    :param initials: key value pairs of initial field values.
    :type initials: ``str=object``
    :returns: form dictionary
    :rtype: dict
    :raises Exception: on API create failure.
    """

    return create_form('workflow_approval', wiid, form_controls,
                       title, content, actions, **initials)


class FleetingClientBadRequestError(Exception):

    def __init__(self, message, response):
        self.message = message
        self.response = response
        self._responses = []

    def response_to_str(self, response, parent_key=""):
        if not isinstance(response, dict):
            return response

        # Find leaves
        for key, value in response.items():
            if not parent_key:
                local_key = key
            else:
                local_key = ".".join([parent_key, key])

            if isinstance(value, dict):
                self.response_to_str(value, local_key)
            else:
                self._responses.append("{}: {}".format(local_key, value))

        return self._responses

    def __str__(self):
        # collect keys
        return "The API request was invalid:\n{}".format(
                "\n".join(self._responses))

class FleetingClient():
    """Abstract base class for all Fleeting API clients.

    Handles authentication and URL generation, which is common to all
    clients.

    :param token: override the company token in the database
    :type token: str (UUID4 format)
    """

    API_ROOT = "https://fleetingforms.io"
    MODEL_ROOT = "forms"
    TRAILING_SLASH = True

    def __init__(self, token=None):
        self.__token = token

    @property
    def headers(self):
        """Headers for authentication to a namespace.

        Make it easy to get namespace authentication headers for this client.

        :returns: authentication headers for use with requests.
        :rtype: dict
        """
        return {'X-FLEETING-TOKEN': self.token}

    @property
    def token(self):
        """Get the token."""
        if not self.__token:
            self.__token = get_token()

        return self.__token

    def url_for(self, action='create', _id=None):
        """Get the URL for an action type.

        Supported actions are ``create``, ``retrieve``, ``list``, ``delete``.

        :param action: the action the url is required form.
        :type action: str
        :param _id: the id of the form to retrieve or delete.
        :type _id: int
        :returns: url for the action and _id.
        :rtype: str
        :raises Exception: Unsupported action if action not supported.
        """
        if action in ['create', 'list']:
            url = "/".join([self.API_ROOT, self.MODEL_ROOT])
        elif action in ['get', 'delete']:
            url ="/".join([self.API_ROOT, self.MODEL_ROOT, str(_id)])
        else:
            raise Exception("Unsupported URL action: {}".format(action))

        if self.TRAILING_SLASH:
            url += "/"

        return url


class FormClient(FleetingClient):
    """The form client class is used to interact with the fleetingforms.io api.

    :param namespace_token: the unique token for the user namespace
    :type token: str (uuid4 format)

    The client supports standard ReSTful actions against the API.  To walk
    through the lifecycle of a form as seen from the api:

    .. code-block:: python

        # Instantiate a new client
        client = FormClient()

        # And define a minimalist form with two buttons.
        form_template = {
            'title': 'Approval Request for More Eggs',
            'content': 'Can we buy more eggs?',
            'form_controls': [],
            'actions': [{'label': 'Yes!'}, {'label': 'No.'}],
        }

        # Create the form using a POST request to the API.
        form = client.create(form_template)

        _id = form['id']
        # print an integer ID unique to the form
        print(form['id'])

        # print the unique URL for the form
        print(form['url'])

        # Retrieve the form to see if the form has been opened
        form = client.get(_id)

        # Check to see if the opened_on field has a datetime
        if form['opened_on']:
            print("The form was opened on {}".format(form['opened_on']))

        # Get a list of all the forms defined in the namespace:
        forms = client.list()
        for form in forms:
            print("Form {} at URL {}".format(form['_id'], form['url']))

        # Delete a form
        deleted = client.delete(_id)
    """

    MODEL_ROOT = "forms"

    def create(self, template={}, auth={}, app={}):
        """Create a new form.

        :param template: the form template.
        :type template: dict
        :param auth: the form authentication parameters.
        :type auth: dict
        :param app: the form appentication parameters.
        :type app: dict
        :returns: form dictionary
        :rtype: dict
        :raises Exception: API failure.
        """

        payload = {
                'template': template,
                'auth': auth,
                'app': app,
            }

        try:
            resp = requests.post(self.url_for('create'),
                                 json=payload,
                                 headers=self.headers)
            if resp.status_code == 201:
                rj = resp.json()
            elif resp.status_code == 400:
                raise FleetingClientBadRequestError(
                        "Invalid HTTP request.",
                        resp.json())
            else:
                raise Exception("HTTP create request status {}".format(
                                    resp.status_code))
        except Exception as e:
            raise

        return rj

    def get(self, _id):
        """Retrieve a specific form from the service.

        :param _id: the ``id`` of the form to retrieve
        :type _id: int
        :returns: form dictionary
        :rtype: dict
        :raises Exception: API failure.
        """
        try:
            resp = requests.get(self.url_for('get', _id), headers=self.headers)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            pass

        return None

    def list(self):
        """List all the forms in this namespace.

        :returns: a list of form dictionaries
        :rtype: [{'id': 1, }, ...]
        :raises Exception: API failure.
        """
        try:
            resp = requests.get(self.url_for('list'), headers=self.headers)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            raise

        return []

    def delete(self, _id):
        """Delete a form from the service.

        :param _id: the ``id`` of the form to delete
        :type _id: int
        :returns: True if deleted, else False
        :rtype: bool
        :raises Exception: API failure.
        """
        try:
            resp = requests.delete(self.url_for('delete', _id),
                                   headers=self.headers)
            if resp.status_code == 204:
                return True
            else:
                raise Exception("Failed to delete: {}".format(resp.text))
        except Exception as e:
            raise Exception("Failed to delete: {}".format(e))

        return False

class NamespaceClient(FleetingClient):
    """The namespace client is used to interact with the fleetingforms.io api.

    :param namespace_token: the unique token for the user namespace
    :type token: str (uuid4 format)

    The client supports standard ReSTful actions against the API.

    .. code-block:: python

        # Instantiate a new client
        client = FormClient()

        # And define a minimalist form with two buttons.
        form_template = {
            'title': 'Approval Request for More Eggs',
            'content': 'Can we buy more eggs?',
            'form_controls': [],
            'actions': [{'label': 'Yes!'}, {'label': 'No.'}],
        }

        # Create the form using a POST request to the API.
        form = client.create(form_template)

        _id = form['id']
        # print an integer ID unique to the form
        print(form['id'])

        # print the unique URL for the form
        print(form['url'])

        # Retrieve the form to see if the form has been opened
        form = client.get(_id)

        # Check to see if the opened_on field has a datetime
        if form['opened_on']:
            print("The form was opened on {}".format(form['opened_on']))

        # Get a list of all the forms defined in the namespace:
        forms = client.list()
        for form in forms:
            print("Form {} at URL {}".format(form['_id'], form['url']))

        # Delete a form
        deleted = client.delete(_id)
    """
    MODEL_ROOT = "namespaces"

    def get(self, _id):
        """Retrieve a specific form from the service.

        :param _id: the ``id`` of the form to retrieve
        :type _id: int
        :returns: form dictionary
        :rtype: dict
        :raises Exception: API failure.
        """
        try:
            resp = requests.get(self.url_for('get', _id), headers=self.headers)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            pass

        return None

    def list(self):
        """List all the namespaces belonging to this token.

        :returns: a list of form dictionaries
        :rtype: [{'id': 1, }, ...]
        :raises Exception: API failure.
        """
        try:
            resp = requests.get(self.url_for('list'), headers=self.headers)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            raise

        return []

    def update(self, _id, data={}):
        """Update a namespace's settings.

        :param _id: the ``id`` of the form to delete
        :type _id: int
        :param data: update payload
        :type data: dict
        :returns: True if updated, else False
        :rtype: bool
        :raises Exception: API failure.
        """
        try:
            resp = requests.put(self.url_for('get', _id),
                                json=data,
                                headers=self.headers)
            if resp.status_code == 200:
                return True
            else:
                raise Exception("Failed to update: {}".format(resp.text))
        except Exception as e:
            raise Exception("Failed to update: {}".format(e))

        return False
