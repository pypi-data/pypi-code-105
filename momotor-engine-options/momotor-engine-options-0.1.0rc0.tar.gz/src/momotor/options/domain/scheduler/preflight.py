import typing
from textwrap import dedent

from momotor.bundles import ResultsBundle
from momotor.bundles.elements.properties import Property
from momotor.bundles.elements.result import Result, Outcome
from momotor.options.option import OptionDefinition, OptionNameDomain
from momotor.options.parser.placeholders import replace_placeholders
from momotor.options.parser.selector import match_by_selector, parse_selector
from momotor.options.providers import Providers
from ._domain import DOMAIN

SCHEDULER_PREFLIGHT_OPTION_NAME = OptionNameDomain('preflight', DOMAIN)

DEFAULT_PREFLIGHT_SELECTOR = '%any error'
DEFAULT_PREFLIGHT_ACTION = 'error'
DEFAULT_PREFLIGHT_OPTION = f'{DEFAULT_PREFLIGHT_SELECTOR} => {DEFAULT_PREFLIGHT_ACTION}'


PREFLIGHT_OPTION = OptionDefinition(
    name=SCHEDULER_PREFLIGHT_OPTION_NAME.name,
    domain=SCHEDULER_PREFLIGHT_OPTION_NAME.domain,
    type='str',
    doc=dedent(f"""\
        A preflight check handled by the scheduler. This allows recipes to indicate situations in which the
        checklet does not have to be executed. 

        Format: "<selector> "=>" <action> [ " " <status message> ]"
                         
        Possible actions are 'run', 'pass', 'pass-secret', 'fail', 'fail-secret', 'skip', 'error' and 'skip-error'.
        
        'run' runs the checklet. When a 'run' action is encountered, no further preflight options are processed
        'pass' and 'pass-secret' will return a 'pass' outcome without running the checklet.
        'fail' and 'fail-secret' will return a 'fail' outcome without running the checklet.
        'skip' and 'skip-error' will return a 'skip' outcome without running the checklet.
        'error' will return an 'error' outcome without running the checklet.
        
        If a results bundle is returned, the properties will contain a 'preflight-trigger' property with the selector
        that triggered the action, a 'source' property with the name of this module, and a 'status' property with the 
        status message, if provided.
        
        'pass-secret', 'fail-secret' add 'secret' property with value True.
        'skip-error' adds 'error-deps' property with value True.
        
        The default preflight check is:
        
        {DEFAULT_PREFLIGHT_OPTION}
        
        This check is executed before any other preflight checks provided in the options.
        
        To override the default action and run the checklet even if one of the dependencies had an error, add  
        at least one 'error' selector, e.g. "error:run" 

        If no preflight check selectors match, the step is executed.

    """),
    multiple=True,
    location=('config', 'recipe', 'step')
)

# Properties for 'pass-secret' and 'fail-secret' actions
SECRET_PROPERTIES = {
    'secret': True,
}

# Properties for 'skip' action
SKIP_PROPERTIES = {
    'skipped': True,
}

# Properties for the 'skip-error' action
SKIP_ERROR_PROPERTIES = {
    **SKIP_PROPERTIES,
    'deps-error': True,
}

ActionType = typing.Tuple[Outcome, typing.Dict]

PREFLIGHT_ACTIONS: typing.Dict[str, typing.Optional[ActionType]] = {
    'run': None,
    'pass': (Outcome.PASS, {}),
    'pass-secret': (Outcome.PASS, SECRET_PROPERTIES),
    'fail': (Outcome.FAIL, {}),
    'fail-secret': (Outcome.FAIL, SECRET_PROPERTIES),
    'skip': (Outcome.SKIP, SKIP_PROPERTIES),
    'error': (Outcome.ERROR, {}),
    'skip-error': (Outcome.SKIP, SKIP_ERROR_PROPERTIES),
}


def create_preflight_result(
    providers: Providers, trigger: str, action: ActionType, status: typing.Optional[str]
) -> typing.Optional[ResultsBundle]:

    """ Create a results bundle for the given action
    """
    outcome, properties = action

    properties = {
        **properties,
        'preflight-trigger': trigger,
        'source': __name__,
    }

    if status:
        properties['status'] = status

    bundle = ResultsBundle()
    bundle.create(
        results=[
            Result(bundle).create(
                step_id=str(providers.task_id),
                outcome=outcome,
                properties=[
                    Property(bundle).create(name=name, value=value)
                    for name, value in properties.items()
                ]
            )
        ]
    )

    return bundle


def preflight_check(providers: Providers) -> typing.Optional[ResultsBundle]:
    """ Check the `preflight@scheduler` option and return a ResultBundle with a result for the task with id
    `task_id` if any pre-flight options activated.

    Returns `None` if the step should run.
    """

    preflight_options = PREFLIGHT_OPTION.resolve(providers)

    # If there are no 'error' condition checks, add the default check as the first one
    has_error_selector = False
    for preflight_option in preflight_options:
        mod, type_, provider, refs, oper, value, remainder = parse_selector(
            replace_placeholders(preflight_option, providers),
            providers.task_id
        )
        if type_ == 'error':
            has_error_selector = True
            break

    if not has_error_selector:
        preflight_options = [DEFAULT_PREFLIGHT_OPTION, *preflight_options]

    for preflight_option in preflight_options:
        match, remaining = match_by_selector(preflight_option, providers)

        remaining = remaining.lstrip()
        if not remaining.startswith('=>'):
            raise ValueError(f"Invalid {PREFLIGHT_OPTION.name} format {preflight_option!r}")

        remaining = replace_placeholders(remaining[2:].strip(), providers)
        if ' ' in remaining:
            action_str, status = remaining.split(' ', 1)
        else:
            action_str, status = remaining, None

        try:
            action = PREFLIGHT_ACTIONS[action_str]
        except KeyError:
            raise ValueError(f"Invalid {PREFLIGHT_OPTION.name} action {action_str!r} in {preflight_option!r}")

        if match:
            if action:
                return create_preflight_result(providers, preflight_option, action, status)
            else:
                break

    return None
