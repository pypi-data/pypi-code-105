"""
This file contains helper methods that are used
across multiple workflow actions:

- Token Management
- Client Helper Function
"""
try:
    from accpac import *
except ImportError:
    pass

import re
import json
import logging
import requests
from pathlib import Path
from logging.handlers import RotatingFileHandler
from collections import OrderedDict
from extools.env import execution_context, EXEC_PS, EXEC_VI

VERSION = '5.2.8'

# Token handling and configuration constants
VI_MODULE = 'REMOTEACTION'
CONFIG_DB_TABLE  = 'VIRAOPT'
CONFIG_VIEW_NAME = '.'.join([VI_MODULE, CONFIG_DB_TABLE])
CONFIG_TOKEN_FIELD = 'TOKEN'
HANDLER_DB_TABLE  = 'VIRAHNDL'
HANDLER_VIEW_NAME = '.'.join([VI_MODULE, HANDLER_DB_TABLE])
LOG_BASE_NAME = 'remote_action'
AGREEMENTS_DB_TABLE = "ADBSIGNA"
AGREEMENTS_VIEW = '.'.join([VI_MODULE, AGREEMENTS_DB_TABLE])
TRANSIENT_DOCS_TABLE = "ADBSIGND"
TRANSIENT_DOCS_VIEW = '.'.join([VI_MODULE, TRANSIENT_DOCS_TABLE])

# Content handling constants
HTML_BODY_RE = re.compile(r'<body[^\>]*>([\s\S]*)<\/body>')

# Shared Constants
ADMIN_USER = "ADMIN"  # only this user can open the management tools

# Token utility methods
def get_token():
    """Get the token from the database.

    :returns: token
    :rtype: str (UUID4 format)
    :raises: Exception - failure to setup view.
    """
    token = ''
    try:
        config_view = openView(CONFIG_VIEW_NAME)
        rc = config_view.recordClear()
        br = config_view.browse("")

        if sum([rc, br, ]):
            raise Exception("failed to open and clear {} config view.".format(
                CONFIG_VIEW_NAME))
        if config_view.fetch() == 0:
            token = config_view.get(CONFIG_TOKEN_FIELD)
    finally:
        config_view.close()
    return token

def set_token(token):
    """Set the token in the company database.

    :param token: token to set.
    :type token: str (UUID4 format)
    :returns: None
    :raises: Exception - failure to set token.
    """
    try:
        config_view = openView(CONFIG_VIEW_NAME)
        rc = config_view.recordClear()
        br = config_view.browse("", 1)
        if sum([rc, br, ]):
            raise Exception("failed to open and clear {} config view.".format(
                CONFIG_VIEW_NAME))

        # remote all existing tokens - updating in place causes locking issue
        # there can only be one for any company
        while config_view.fetch() == 0:
            config_view.delete()

        config_view.recordClear()
        if config_view.recordGenerate() != 0:
            raise Exception("failed to generate new token record.")

        config_view.put(CONFIG_TOKEN_FIELD, token)

        if config_view.insert() != 0:
            raise Exception("token field insert failed.")
    finally:
        config_view.close()
    return token

# Logging helper methods
def debug_enabled():
    debug_path = Path(getOrgPath(), "{}.debug".format(LOG_BASE_NAME))
    return debug_path.exists()

def get_log_path(name, uniquifier=""):
    log_name = "{}.log".format(LOG_BASE_NAME)
    if uniquifier:
        log_name = "{}.{}.log".format(LOG_BASE_NAME, uniquifier)
    return Path(getOrgPath(), log_name)

__loggers = {}

def get_logger(name, uniquifier=""):
    global __loggers

    key = "{}{}".format(name, uniquifier)
    if key not in __loggers:

        log_path = get_log_path(name, uniquifier)
        ralog_path = get_log_path(name)

        level = logging.INFO
        if debug_enabled():
            level = logging.DEBUG

        logging.basicConfig(
                level=level,
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%Y-%m-%dT%H:%M:%S',
                handlers=[RotatingFileHandler(
                    filename=str(log_path),
                    backupCount=5,
                    maxBytes=10*1024*1024),
                    RotatingFileHandler(
                    filename=str(ralog_path),
                    backupCount=5,
                    maxBytes=10*1024*1024), ],
            )

    # silence urllib
    ulog = logging.getLogger("requests.packages.urllib3.connectionpool")
    ulog.setLevel(logging.WARN)

    __loggers[key] = logging.getLogger(name)

    return __loggers[key]

# Workflow helper methods
def get_user(a4wuser, userid):
    """Get a user's email from the a4wuser view.

    :param a4wuser: An open AS0003 view
    :type a4wuser: accpac.View
    :param userid: The Sage User ID.
    :type userid: str
    :returns: username and email if found, otherwise None.
    :rtype: (str, str)
    """
    user = None
    a4wuser.put("USERID", userid)
    if a4wuser.read() == 0:
        email = a4wuser.get("EMAIL1").strip()
        if not email:
            email = a4wuser.get("EMAIL2").strip()
        user = (userid, email)
    return user

def get_users_for_group(a4wuser, vigroupd, groupid):
    """Get the users and their emails for a vi group.

    :param a4wuser: An open AS0003 view
    :type a4wuser: accpac.View
    :param vigroupd: An open VI0024 view
    :type a4wuser: accpac.View
    :param groupid: The Extender Group ID.
    :returns: list of usernames and email tuples found.
    :rtype: [(str, str)]
    """
    users = []
    vigroupd.order(0) # GROUP/USERID
    vigroupd.recordClear()
    vigroupd.browse('GROUP="{}"'.format(groupid))
    while vigroupd.fetch() == 0:
        user = get_user(a4wuser, vigroupd.get("USERID"))
        if user:
            users.append(user)
    return users

def resolve_users(emails):
    """Resolve a ; separated list to a list of (username, email) tuples.

    Given a ; separated list, resolve to Sage Usernames and User Emails.
    If an email is provided directly, return the email as the username.

    Consider a configuration in which:

    - There is a group MYGRP composed of three users:

      - ANNE (anne@a.com), BOB (bobby@a.com), CHRIS (cbinckly@a.com)

    - Other users are defined in Sage but are not members of the group.

      - DARREN (darren@a.com), ESTHER (esther@a.com), FRANK (frank@a.com)

    - And some clients are not in the Sage database at all:

      - user1@client.com, user2@client.com

    .. code-block:: python

        >>> resolve_users("MYGRP;DARREN;user1@client.com")
        [(ANNE, anne@a.com), (BOB, bobby@a.com), (CHRIS, cbinckly@a.com),
         (DARREN, darren@a.com), (user1@client.com, user1@client.com)]

    :param emails: ';' separated list
    :type emails: str
    :returns: list of (username, email) tuples
    :rtype: [(str, str)]
    """
    users = []
    emails = [e.strip() for e in emails.split(";") if e]

    a4wuser = openView("AS0003")
    vigroupd = openView("VI0024")

    for email in emails:
        if re.search(r'[^@]+@.+\.\w+', email):
            users.append((email, email, ))
        elif email:
            user = get_user(a4wuser, email)
            if user:
                users.append(user)
            else:
                users += get_users_for_group(
                        a4wuser, vigroupd, email)

    a4wuser.close()
    vigroupd.close()

    return users

def user_for_email(email):
    """Find the user for a given email.

    :param email: email address
    :type email: str
    :returns: username
    :rtype: str
    """
    a4wuser = openView("AS0003")
    a4wuser.recordClear()
    a4wuser.browse("", 1)
    user = ""
    while a4wuser.fetch() == 0:
        if email in [a4wuser.get("EMAIL1"), a4wuser.get("EMAIL2")]:
            user = a4wuser.get("USERID")
            break
    a4wuser.close()

    return user

def render_title_and_content_for(template_name, workflow):
    """Hijack the Email templates for workflow form content.

    Renders an email template, resolving the content in the context
    of the provided workflow object and its associated view.

    The HTML body of the template must be extracted as nested <html>
    are invalid.

    :param template_name: VIMSG template name to render
    :type template_name: str
    :param workflow: workflow object to use for resolution
    :type worflow: accpac.Workflow
    :returns: (title, content)
    :rtype: (str, str)
    """
    email_renderer = Email()
    email_renderer.load(template_name)
    email_renderer.replace("", workflow.wi.getView())
    title = ReplaceFields(workflow.resolve(email_renderer.subject))
    content = ""
    if email_renderer.htmlBody:
        html = ReplaceFields(workflow.resolve(email_renderer.htmlBody))
        match = HTML_BODY_RE.search(html)
        if match:
            content = match.group(1)
        else:
            raise RuntimeError("failed to extract HTML body from rendered "
                               "content.")
    else:
        content = ReplaceFields(workflow.resolve(email_renderer.textBody))
    return title, content

def parse_action_parameter(value):
    """Parse the action parameter (P4) of a workflow action.

    P4 for the workflow actions defines the button labels and progress to steps
    in a separated key value pair string format::

        <label>=<next step>,<label>=<next step>
        Approve=Approved+RTP,Rejected=Rejected

    :param value: the action parameter as inputinto the template.
    :type value: string
    :returns: label to next step name mappings
    :rtype: collections.OrderedDict
    """
    actions = OrderedDict()
    steps = value.split(',')
    for step in steps:
        label, next_step = step.split('=')
        if not next_step:
            raise ValueError("The step to proceed to must be set.")
        actions[label] = next_step
    return actions

def _alert(message):
    """Show an alert to the user.

    When running in VI, the alert is shown in a message box.
    """
    if execution_context() == EXEC_VI:
        showMessageBox("Remote Actions\n\n{}".format(message))
    logger = get_logger("remote_actions")
    logger.info(message)

def _error(message):
    """Register an error in the process.

    When running in VI, the error is shown in a message box.
    """
    if execution_context() == EXEC_VI:
        showMessageBox("Remote Actions - Error\n\n{}".format(message))
    logger = get_logger("remote_actions")
    logger.exception(message)
