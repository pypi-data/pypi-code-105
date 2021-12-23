# Copyright 2021 Henix, henix.fr
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""opentf-ctl"""

import csv
import logging
import os
import re
import sys

from time import sleep
from urllib.parse import urlparse

import jwt
import requests

from opentf.tools.ctlcommons import _is_command, _get_value
from opentf.tools.ctlconfig import (
    read_configuration,
    config_cmd,
    print_config_help,
    CONFIG,
    HEADERS,
)


########################################################################

# pylint: disable=broad-except

WATCHED_EVENTS = (
    'ExecutionCommand',
    'ExecutionResult',
    'ExecutionError',
    'ProviderCommand',
    'GeneratorCommand',
)

AUTOVARIABLES_PREFIX = 'OPENTF_RUN_'

WARMUP_DELAY = 5
REFRESH_DELAY = 10


########################################################################
# Help messages

GENERAL_HELP = '''opentf-ctl controls the OpenTestFactory orchestrators.

Basic Commands:
  get workflows                List active and recent workflows
  run workflow {filename}      Start a workflow
  get workflow {workflow_id}   Get a workflow status
  kill workflow {workflow_id}  Cancel a running workflow

Agent Commands:
  get agents                   List registered agents
  delete agent {agent_id}      De-register an agent

Token Commands:
  generate token using {key}   Interactively generate a signed token

Advanced Commands:
  get subscriptions            List active subscriptions

Other Commands:
  config                       Modify current opentf-tools configuration
  version                      List the tools version

Usage:
  opentf-ctl <command> [options]

Use "opentf-ctl <command> --help" for more information about a given command.
Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

OPTIONS_HELP = '''
The following environment variables override the defaults, if not overridden by options:

  OPENTF_CONFIG: Path to the opentfconfig file to use for CLI requests
  OPENTF_TOKEN: Bearer token for authentication to the orchestrator

The following options can be passed to any command:

  --token='': Bearer token for authentication to the orchestrator
  --user='': The name of the opentfconfig user to use
  --orchestrator='': The name of the opentfconfig orchestrator to use
  --context='': The name of the opentfconfig context to use
  --insecure-skip-tls-verify=false: If true, the server's certificate will not be checked for validity.  This will make your HTTPS connections insecure
  --opentfconfig='': Path to the opentfconfig file to use for CLI requests
'''

VERSION_HELP = '''
List the tools version

Example:
  # Display the version of the tools
  opentf-ctl version

Usage:
  opentf-ctl version [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

GET_SUBSCRIPTIONS_HELP = '''List active subscriptions on the eventbus

Example:
  # List the subscriptions
  opentf-ctl get subscriptions

Usage:
  opentf-ctl get subscriptions [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

GET_AGENTS_HELP = '''List registered agents

Example:
  # List the agents
  opentf-ctl get agents

Usage:
  opentf-ctl get agents [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

DELETE_AGENT_HELP = '''De-register an active agent

Example:
  # De-register the specified agent
  opentf-ctl delete agent 9ea3be45-ee90-4135-b47f-e66e4f793383

Usage:
  opentf-ctl delete agent AGENT_ID [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

RUN_WORKFLOW_HELP = '''Start a workflow

Examples:
  # Start the workflow defined in my_workflow.yaml
  opentf-ctl run workflow my_workflow.yaml

  # Start the workflow and wait until it completes
  opentf-ctl run workflow my_workflow.yaml --wait

  # Start the workflow and define an environment variable
  opentf-ctl run workflow my_workflow.yaml -e TARGET=example.com

  # Start a workflow and provide environment variables defined in a file
  opentf-ctl run workflow my_workflow.yaml -e variables

  # Start a workflow and provide a localy-defined environment variable
  export OPENTF_RUN_MYVAR=my_value
  opentf-ctl run workflow my_workflow.yaml  # variable 'MYVAR' will be defined

  # Start the wokflow and provide a local file
  opentf-ctl run workflow my_workflow.yaml -f key=./access_key.pem

Environment variables:
  Environment variables with an 'OPENTF_RUN_' prefix will be defined without the prefix in the workflow and while running commands in execution environment.

Options:
  -e var=value: 'var' will be defined in the workflow and while running commands in execution environment.
  -e path/to/file: variables defined in file will be defined in the workflow and while running commands in execution environment.  'file' must contain one variable definition per line, of the form 'var=value'.
  -f name=path/to/file: the specified local file will be available for use by the workflow.  'name' is the file name specified in the `resources.files` part of the workflow.
  --wait: wait for workflow completion.
  --step_depth=1: show nested steps to the given depth (only used with --wait).
  --job_depth=1: show nested jobs to the given depth (only used with --wait).

Usage:
  opentf-ctl run workflow NAME [-e var=value]... [-e path/to/file] [-f name=path/to/file]... [--wait] [--job_depth=value] [--step_depth=value] [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

GET_WORKFLOW_HELP = '''Get a workflow status

Examples:
  # Get the current status of a workflow
  opentf-ctl get workflow 9ea3be45-ee90-4135-b47f-e66e4f793383

  # Get the status of a workflow and wait until its completion
  opentf-ctl get workflow 9ea3be45-ee90-4135-b47f-e66e4f793383 --watch

  # Get the status of a workflow, showing first-level nested steps
  opentf-ctl get workflow 9ea3be45-ee90-4135-b47f-e66e4f793383 --step_depth=2

Options:
  --step_depth=1: show nested steps to the given depth.
  --job_depth=1: show nested jobs to the given depth.
  --watch: wait until workflow completion or cancellation, displaying status updates as they occur.

Usage:
  opentf-ctl get workflow WORKFLOW_ID [--step_depth=value] [--job_depth=value] [--watch] [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

GET_WORKFLOWS_HELP = '''List active and recent workflows

Examples:
  # List the IDs of active and recent workflows
  opentf-ctl get workflows

  # Get the status of active and recent workflows
  opentf-ctl get workflows --output=wide

Options:
  --output=wide: show additional information.

Usage:
  opentf-ctl get workflows [--output=wide] [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

KILL_WORKFLOW_HELP = '''Kill a running workflow

Example:
  # Kill the specified workflow
  opentf-ctl kill workflow 9ea3be45-ee90-4135-b47f-e66e4f793383

Usage:
  opentf-ctl kill workflow WORKFLOW_ID [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''

GENERATE_TOKEN_HELP = '''Generate a signed token

Example:
  # Generate token interactively
  opentf-ctl generate token using path/to/private.pem

Usage:
  opentf-ctl generate token using NAME [options]

Use "opentf-ctl options" for a list of global command-line options (applies to all commands).
'''


########################################################################
# Helpers


def _make_hostport(service):
    """Adjust server port for service."""
    server = CONFIG['orchestrator']['server']
    if 'ports' in CONFIG['orchestrator']:
        port = str(CONFIG['orchestrator']['ports'].get(service, ''))
        if port:
            url = urlparse(server)
            new = url._replace(netloc=url.netloc.split(':')[0] + ':' + port)
            server = new.geturl()
    return server.strip('/')


def _receptionist():
    return _make_hostport('receptionist')


def _eventbus():
    return _make_hostport('eventbus')


def _observer():
    return _make_hostport('observer')


def _killswitch():
    return _make_hostport('killswitch')


def _agentchannel():
    return _make_hostport('agentchannel')


def _could_not_connect(target):
    logging.error(
        'Could not connect to the orchestrator.  Is the orchestrator running?'
    )
    logging.error('(Attempting to reach %s)', target)
    sys.exit(2)


########################################################################
# Eventbus


def list_subscriptions():
    """List all active subscriptions.

    Outputs information in CSV format (using ',' as a column delimiter).

    # Raised exceptions

    Abort with an error code 1 if the orchestrator replied with a non-ok
    code.

    Abort with an error code 2 if another error occurred.
    """
    try:
        what = requests.get(
            _eventbus() + '/subscriptions',
            headers=HEADERS,
            verify=not CONFIG['orchestrator']['insecure-skip-tls-verify'],
        )
        if what.status_code == 200:
            what = what.json()
        else:
            logging.error(
                'Could not get subscription list, got %d: %s.',
                what.status_code,
                what.text,
            )
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        _could_not_connect(_eventbus())
    except Exception as err:
        logging.error('Could not get subscription list: %s.', err)
        sys.exit(2)

    writer = csv.writer(sys.stdout)
    writer.writerow(('name', 'endpoint', 'creation', 'count', 'subscription'))
    for _, manifest in what['items'].items():
        metadata = manifest['metadata']
        spec = manifest['spec']
        writer.writerow(
            (
                metadata['name'],
                spec['subscriber']['endpoint'],
                metadata['creationTimestamp'][:22],
                manifest['status']['publicationCount'],
                ':'.join(metadata['annotations'].values()),
            )
        )


def list_agents():
    """List all active agents.

    Outputs information in CSV format (using ',' as a column delimiter).

    # Raised exceptions

    Abort with an error code 1 if the orchestrator replied with a non-ok
    code.

    Abort with an error code 2 if another error occurred.
    """
    try:
        what = requests.get(
            _agentchannel() + '/agents',
            headers=HEADERS,
            verify=not CONFIG['orchestrator']['insecure-skip-tls-verify'],
        )
        if what.status_code == 200:
            what = what.json()
        else:
            logging.error(
                'Could not get agent list, got %d: %s.',
                what.status_code,
                what.text,
            )
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        _could_not_connect(_agentchannel())
    except Exception as err:
        logging.error('Could not get agent list: %s.', err)
        sys.exit(2)

    # apiVersion: opentestfactory.org/v1alpha1
    # kind: AgentRegistration
    # metadata:
    #   creationTimestamp': 2021-12-03T17:52:36.335360
    #   name: test agent
    # spec:
    #   encoding: utf-8
    #   script_path': '/where/to/put/scripts'
    #   tags: ['windows', 'robotframework']
    # status:
    #   communicationCount: 0
    #   communicationStatusSummary: {}
    #   lastCommunicationTimestamp: '2021-12-03T17:53:41.560939'
    #   currentJobID: currently running job ID or None if idle
    writer = csv.writer(sys.stdout)
    writer.writerow(
        (
            'NAME',
            'AGENT_ID',
            'TAGS',
            'REGISTRATION_TIMESTAMP',
            'LAST_SEEN_TIMESTAMP',
            'RUNNING_JOB',
        )
    )
    for agent_id, manifest in what['items'].items():
        metadata = manifest['metadata']
        spec = manifest['spec']
        writer.writerow(
            (
                metadata['name'],
                agent_id,
                ':'.join(spec['tags']),
                metadata['creationTimestamp'][:22],
                manifest['status']['lastCommunicationTimestamp'][:22],
                manifest['status'].get('currentJobID', ''),
            )
        )


def delete_agent(agent_id):
    """Deregister agent."""
    try:
        what = requests.delete(
            _agentchannel() + '/agents/' + agent_id,
            headers=HEADERS,
            verify=not CONFIG['orchestrator']['insecure-skip-tls-verify'],
        )
        if what.status_code == 200:
            what = what.json()
        elif what.status_code == 404:
            logging.error('Could not delete agent %s: not found.', agent_id)
            sys.exit(1)
        else:
            logging.error(
                'Could not delete agent %s, got %d: %s.',
                agent_id,
                what.status_code,
                what.text,
            )
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        _could_not_connect(_agentchannel())
    except Exception as err:
        logging.error('Could not delete agent: %s.', err)
        sys.exit(2)
    print(what['message'])


def _file_not_found(name, err):
    logging.error('File not found: %s.', name)
    logging.debug('Error is: %s.', err)
    sys.exit(2)


def _read_variables_file(file, variables):
    """Read file and add variables.

    Abort with an error code 2 if the file does not exist or contains
    invalid content.
    """
    try:
        with open(file, 'r', encoding='utf-8') as varfile:
            for line in varfile:
                if '=' not in line:
                    logging.error(
                        'Invalid format in file %s, was expecting var=value.',
                        file,
                    )
                    sys.exit(2)
                var, _, value = line.strip().partition('=')
                variables[var] = value
    except FileNotFoundError as err:
        _file_not_found(file, err)


def _add_files(args, files):
    """Handling -f file command-line options."""
    process = False
    for option in args:
        if option == '-f':
            process = True
            continue
        if process:
            process = False
            name, path = option.split('=')
            try:
                files[name] = open(path, 'rb')
            except FileNotFoundError as err:
                _file_not_found(path, err)


def _add_variables(args, files):
    """Handling -e file and -e var=value command-line options."""
    # OPENTF_CONFIG and OPENTF_TOKEN are explicitly excluded to prevent
    # unexpected leak
    variables = {
        key[len(AUTOVARIABLES_PREFIX) :]: value
        for key, value in os.environ.items()
        if key.startswith(AUTOVARIABLES_PREFIX)
        and key not in ('OPENTF_CONFIG', 'OPENTF_TOKEN')
    }
    process = False
    for option in args:
        if option == '-e':
            process = True
            continue
        if process:
            process = False
            if '=' in option:
                var, _, value = option.partition('=')
                variables[var] = value
            else:
                _read_variables_file(option, variables)
    if variables:
        files['variables'] = '\n'.join(f'{k}={v}' for k, v in variables.items())


def _emit_wide_workflow(workflow_id):
    response = _get_first_page(workflow_id)
    if response.status_code == 200:
        status = response.json()['details']['status']
        what = response.json()['details']['items']
        if what:
            firstseen = what[0]['metadata']['creationTimestamp']
            if what[0]['kind'] == 'Workflow':
                name = what[0]['metadata']['name']
            else:
                name = ''
            print(','.join((workflow_id, status, firstseen, name)))
        else:
            print(','.join((workflow_id, '', '', '')))
    else:
        print(workflow_id, 'got response code %d' % response.status_code)


def list_workflows():
    """List active and recent workflows."""
    try:
        response = requests.get(
            _observer() + '/workflows',
            headers=HEADERS,
            verify=not CONFIG['orchestrator']['insecure-skip-tls-verify'],
        )
        if response.status_code != 200:
            if response.status_code in (404, 405):
                logging.error(
                    'Could not get workflows list.  Maybe an outdated orchestrator version.'
                )
            else:
                logging.error(
                    'Cound not get workflows list.  Return code was %d.',
                    response.status_code,
                )
        workflows = response.json()
        wide = '--output=wide' in sys.argv or ('-o' in sys.argv and 'wide' in sys.argv)
        if wide:
            print('WORKFLOW_ID,STATUS,FIRST_SEEN_TIMESTAMP,WORKFLOW_NAME')
        else:
            print('WORKFLOW_ID')
        for workflow_id in workflows['details']['items']:
            if wide:
                _emit_wide_workflow(workflow_id)
            else:
                print(workflow_id)

    except requests.exceptions.ConnectionError:
        _could_not_connect(_observer())
    except Exception as err:
        logging.error('Could not get list of workflows: %s.', err)
        sys.exit(2)


def run_workflow(workflow_name):
    """Run a workflow.

    # Required parameters

    - workflow_name: a file name

    # Returned value

    Returns the workflow ID if everything was OK.

    # Raised exceptions

    Abort with an error code of 1 if the workflow was not properly
    received by the orchestrator.

    Abort with an error code of 2 if a parameter was invalid (file not
    found or invalid format).
    """
    try:
        files = {'workflow': open(workflow_name, 'r', encoding='utf-8')}
        _add_files(sys.argv[4:], files)
        _add_variables(sys.argv[4:], files)

        result = requests.post(
            _receptionist() + '/workflows',
            files=files,
            headers=HEADERS,
            verify=not CONFIG['orchestrator']['insecure-skip-tls-verify'],
        )
        if result.status_code == 201:
            print('Workflow', result.json()['details']['workflow_id'], 'is running.')
        else:
            logging.error(result.json()['message'])
            if result.json().get('details'):
                logging.error(result.json()['details'].get('error'))
            sys.exit(1)
    except FileNotFoundError as err:
        _file_not_found(workflow_name, err)
    except requests.exceptions.ConnectionError:
        _could_not_connect(_receptionist())
    except Exception as err:
        logging.error('Could not start workflow: %s.', err)
        sys.exit(2)

    if '--wait' in sys.argv:
        sleep(WARMUP_DELAY)
        get_workflow(result.json()['details']['workflow_id'], True)


def _emit_prefix(event):
    print(
        '[%s]' % event['metadata']['creationTimestamp'][:-7],
        '[job %s] ' % event['metadata']['job_id'],
        end='',
    )


def _emit_command(event, silent):
    if event['metadata']['step_sequence_id'] == -1:
        _emit_prefix(event)
        print(
            'Requesting execution environment providing',
            event['runs-on'],
            'for job',
            repr(event['metadata']['name']),
        )
    elif event['metadata']['step_sequence_id'] == -2:
        _emit_prefix(event)
        print(
            'Releasing execution environment for job',
            repr(event['metadata']['name']),
        )
    elif not silent:
        _emit_prefix(event)
        print(' ' * (len(event['metadata'].get('step_origin', []))), end='')
        print('Running command', event['scripts'])


def _emit_result(event, silent):
    for item in event.get('logs', []):
        _emit_prefix(event)
        print(item)
    if event['status'] == 0 or silent:
        return
    _emit_prefix(event)
    print('Status code was:', event['status'])


def _show_events(items, step_depth, job_depth):
    """Show watched events.

    Can be used to show partial items.
    """
    cancelation_event = None
    for event in items:
        silent = False
        if event['kind'] == 'Workflow':
            print('Workflow', event['metadata']['name'])
            continue
        if event['kind'] == 'WorkflowCanceled':
            cancelation_event = event
        if event['kind'] not in WATCHED_EVENTS:
            continue
        if event['kind'] == 'ExecutionError':
            _emit_prefix(event)
            print(event.get('details', {}).get('error'))
            continue

        if job_depth and len(event['metadata'].get('job_origin', [])) >= job_depth:
            silent = True
        elif step_depth and len(event['metadata'].get('step_origin', [])) >= step_depth:
            silent = True

        if event['kind'] == 'ExecutionResult':
            _emit_result(event, silent)
            continue

        if event['kind'] == 'ExecutionCommand':
            _emit_command(event, silent)
            continue

        if not silent:
            _emit_prefix(event)
            print(' ' * (len(event['metadata'].get('step_origin', []))), end='')
            print('Running action', event['metadata']['name'])
    return cancelation_event


def _get_first_page(workflow_id):
    return requests.get(
        _observer() + '/workflows/' + workflow_id + '/status',
        headers=HEADERS,
        verify=not CONFIG['orchestrator']['insecure-skip-tls-verify'],
    )


def _get_worflow_status(workflow_id):
    try:
        response = _get_first_page(workflow_id)
    except requests.exceptions.ConnectionError:
        _could_not_connect(_observer())
    except Exception as err:
        logging.error('Could not get workflow: %s.', err)
        sys.exit(2)

    if response.status_code == 404:
        logging.error(
            'Could not find workflow %s.  The ID is incorrect or too recent or too old.',
            workflow_id,
        )
        sys.exit(1)
    if response.status_code != 200:
        logging.error(
            'Could not get workflow %s.  Got status code %d (%s).',
            workflow_id,
            response.status_code,
            response.text,
        )
        sys.exit(1)

    status = response.json()
    while 'next' in response.links:
        response = requests.get(
            response.links['next']['url'],
            headers=HEADERS,
            verify=not CONFIG['orchestrator']['insecure-skip-tls-verify'],
        )
        status['details']['items'] += response.json()['details']['items']
    return status


def get_workflow(workflow_id, watch=False):
    """Get a workflow.

    # Required parameters

    - workflow_id: a string

    # Optional parameters

    - watch: a boolean (False by default)

    # Returned value

    The current workflow status.

    # Raised exceptions

    Abort with an error code 1 if the workflow could not be found on the
    orchestrator.

    Abort with an error code 2 if another error occurred.
    """
    ensure_uuid(workflow_id)

    status = _get_worflow_status(workflow_id)
    current_item = 0
    job_depth = int(_get_value('--job-depth=') or 1)
    step_depth = int(_get_value('--step-depth=') or 1)

    while True:
        cancelation_event = _show_events(
            status['details']['items'][current_item:],
            job_depth=job_depth,
            step_depth=step_depth,
        )
        if not watch:
            break
        if status['details']['status'] != 'RUNNING':
            break
        current_item = len(status['details']['items'])
        while len(status['details']['items']) <= current_item:
            sleep(REFRESH_DELAY)
            status = _get_worflow_status(workflow_id)

    workflow_status = status['details']['status']
    if workflow_status == 'DONE':
        print('Workflow completed successfully.')
    elif workflow_status == 'RUNNING':
        print('Workflow is running.')
    elif workflow_status == 'FAILED':
        if (
            cancelation_event
            and cancelation_event.get('details', {}).get('status') == 'cancelled'
        ):
            print('Workflow cancelled.')
        else:
            print('Workflow failed.')
    else:
        logging.warning(
            'Unexpected workflow status: %s (was expecting DONE, RUNNING, or FAILED).',
            workflow_status,
        )


def kill_workflow(workflow_id):
    """Kill workflow.

    # Required parameter

    - workflow_id: a non-empty string (an UUID)

    # Raised exceptions

    Abort with an error code 1 if the orchestrator replied with an
    unexpected status code (!= 200).

    Abort with an error code 2 if an error occurred while contacting the
    orchestrator.
    """
    ensure_uuid(workflow_id)
    try:
        response = requests.delete(
            _killswitch() + '/workflows/' + workflow_id,
            headers=HEADERS,
            verify=not CONFIG['orchestrator']['insecure-skip-tls-verify'],
        )
    except requests.exceptions.ConnectionError:
        _could_not_connect(_killswitch())
    except Exception as err:
        logging.error('Could not kill workflow: %s.', err)
        sys.exit(2)
    if response.status_code == 200:
        print(f'Killing workflow {workflow_id}.')
    else:
        logging.error(
            'Could not kill workflow %s.  Got status code %d (%s).',
            workflow_id,
            response.status_code,
            response.text,
        )
        sys.exit(1)


def generate_token(privatekey):
    """Generate JWT token.

    # Required parameters

    - privatekey: a non-empty string (a file name)

    # Raised exceptions

    Abort with an error code 2 if something went wrong.
    """
    try:
        with open(privatekey, 'r', encoding='utf-8') as keyfile:
            pem = keyfile.read()
    except FileNotFoundError:
        logging.error('The specified private key could not be found: %s.', privatekey)
        sys.exit(2)

    algorithm = (
        input('Please specify an algorithm (RS512 if unspecified): ').strip() or 'RS512'
    )
    print('The specified algorithm is:', algorithm)
    while not (
        issuer := input(
            'Please enter the issuer (your company or department): '
        ).strip()
    ):
        logging.warning('The issuer cannot be empty.')
    while not (
        subject := input(
            'Please enter the subject (you or the person you are making this token for): '
        )
    ):
        logging.warning('The subject cannot be empty.')

    try:
        token = jwt.encode({'iss': issuer, 'sub': subject}, pem, algorithm=algorithm)
    except NotImplementedError:
        logging.error('Algorithm not supported: %s.', algorithm)
        sys.exit(2)
    except Exception as err:
        logging.error('Could not generate token: %s.', err)
        sys.exit(2)

    print('The signed token is:')
    print(token)


def get_tools_version():
    """
    Prints in the console the current version details.
    """

    from importlib.metadata import version
    from pkg_resources import parse_version

    fullversion = parse_version(version('opentf-tools'))
    print(
        f'Tools Version: version.Info{{Major:"{fullversion.major}", Minor: "{fullversion.minor}", FullVersion: "{fullversion}"}}'
    )


########################################################################
# Helpers


def ensure_uuid(parameter):
    """Ensure parameter is a valid UUID.

    Abort with error code 2 if `parameter` is not a valid UUID.
    """
    if not re.match(r'^[a-f0-9-]+$', parameter):
        logging.error('Parameter %s is not a valid UUID.', parameter)
        sys.exit(2)


def print_help(args):
    """Display help."""
    if _is_command('options', args):
        print(OPTIONS_HELP)
    if _is_command('version', args):
        print(VERSION_HELP)
    elif _is_command('get subscriptions', args):
        print(GET_SUBSCRIPTIONS_HELP)
    elif _is_command('run workflow', args):
        print(RUN_WORKFLOW_HELP)
    elif _is_command('get workflows', args):
        print(GET_WORKFLOWS_HELP)
    elif _is_command('get workflow', args):
        print(GET_WORKFLOW_HELP)
    elif _is_command('kill workflow', args):
        print(KILL_WORKFLOW_HELP)
    elif _is_command('generate token', args):
        print(GENERATE_TOKEN_HELP)
    elif _is_command('get agents', args):
        print(GET_AGENTS_HELP)
    elif _is_command('delete agent', args):
        print(DELETE_AGENT_HELP)
    elif _is_command('config', args):
        print_config_help(args)
    elif len(args) == 2:
        print(GENERAL_HELP)
    else:
        logging.error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)


########################################################################
# Main


def main():
    """Process command."""
    if len(sys.argv) == 1:
        print(GENERAL_HELP)
        sys.exit(1)
    if sys.argv[-1] == '--help':
        print_help(sys.argv)
        sys.exit(0)

    if _is_command('options', sys.argv):
        print(OPTIONS_HELP)
        sys.exit(0)

    if _is_command('version', sys.argv):
        get_tools_version()
        sys.exit(0)

    if _is_command('generate token using _', sys.argv):
        generate_token(sys.argv[4])
        sys.exit(0)

    if _is_command('get subscriptions', sys.argv):
        read_configuration()
        list_subscriptions()
    elif _is_command('get workflows', sys.argv):
        read_configuration()
        list_workflows()
    elif _is_command('run workflow _', sys.argv):
        read_configuration()
        run_workflow(sys.argv[3])
    elif _is_command('get workflow _', sys.argv):
        read_configuration()
        get_workflow(sys.argv[3], '--watch' in sys.argv)
    elif _is_command('kill workflow _', sys.argv):
        read_configuration()
        kill_workflow(sys.argv[3])
    elif _is_command('get agents', sys.argv):
        read_configuration()
        list_agents()
    elif _is_command('delete agent _', sys.argv):
        read_configuration()
        delete_agent(sys.argv[3])
    elif _is_command('config _', sys.argv):
        config_cmd()
    else:
        logging.error('Unknown command.  Use --help to list known commands.')
        sys.exit(1)


if __name__ == '__main__':
    main()
