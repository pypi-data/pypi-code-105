import asyncio
import copy

import dict_tools.differ as differ

# Reconciliation loop stops after MAX_RERUNS_WO_CHANGE reruns without change.
# This is to make sure we do not retry forever on failures that cannot be fixed by
# reconciliation.
# TODO: For now there is no way to differentiate between "failures" that can be fixed
# by reconciliation (re-runs) or not. Plugins will be enhanced to return 'pending'
# result for failures that can be fixed by re-conciliation.
MAX_RERUNS_WO_CHANGE = 3
# Sleep time in seconds between re-runs
DEFAULT_RECONCILE_WAIT = 3
# Dictionary keeping state's reconcile wait time in seconds
_state_to_sleep_map = {}


async def loop(
    hub,
    name,
    sls_sources,
    render,
    runtime,
    cache_dir,
    sls,
    test,
    acct_file,
    acct_key,
    acct_profile,
):
    """
    This loop attempts to apply states.
    This function returns once all the states are successful or after MAX_RERUNS_WO_CHANGE, whichever occur first.
    The sleep time between each attempt will be determined by a plugin and might change between each iterations.
    Reconciliation is required if the state has pending changes (present) or result that is not 'True'.
    TODO: this is till the plugins implement a pending state and other failure values that should
    TODO: not be re-conciliated
    :param hub:
    :param name:
    :param sls_sources:
    :param render:
    :param runtime:
    :param cache_dir:
    :param sls:
    :param test:
    :param acct_file:
    :param acct_key:
    :param acct_profile:
    :return: dictionary { "re_runs_count": <number of re-runs that occurred>,
                "require_re_run": <True/False whether the last run require more reconciliation> }
    """
    last_run = hub.idem.RUNS[name]["running"]
    if has_passed(last_run):
        return {"re_runs_count": 0, "require_re_run": False}

    # Populate wait time algorithm and values for the different states
    # in this run. State has to define __reconciliation_wait__
    # with values such as:
    # { "exponential": {"wait_in_seconds": 2, "multiplier": 10} }
    # { "static": {"wait_in_seconds": 3} }
    # { "random": {"min_value": 1, "max_value": 10} }
    populate_wait_times(hub, last_run)

    tag_to_old_state_map = populate_old_states(last_run)

    count = 0
    count_wo_change = 0
    while count_wo_change < MAX_RERUNS_WO_CHANGE:
        sleep_time_sec = get_max_wait_time(hub, last_run, count)
        hub.log.debug(f"Sleeping {sleep_time_sec} seconds for {name}")
        await asyncio.sleep(sleep_time_sec)

        count = count + 1
        hub.log.debug(f"Retry {count} for {name}")
        await hub.idem.state.apply(
            name=name,
            sls_sources=sls_sources,
            render=render,
            runtime=runtime,
            subs=["states"],
            cache_dir=cache_dir,
            sls=sls,
            test=test,
            acct_file=acct_file,
            acct_key=acct_key,
            acct_profile=acct_profile,
        )

        current_run = hub.idem.RUNS[name]["running"]
        if has_passed(current_run):
            update_changes(hub, current_run, tag_to_old_state_map)
            return {"re_runs_count": count, "require_re_run": False}

        if is_same_result(last_run, current_run):
            count_wo_change = count_wo_change + 1
        else:
            # reset the count w/o changes upon a change
            count_wo_change = 0

        last_run = current_run

    hub.log.debug(
        f"Reconciliation loop returns after {count} runs total, and {count_wo_change} runs without any change."
    )

    update_changes(hub, last_run, tag_to_old_state_map)
    return {
        "re_runs_count": count,
        "require_re_run": True,
    }


def has_passed(runs):
    # If result is not True or there are changes - then return false and reconcile
    for tag in runs:
        if is_pending(runs[tag]):
            return False
    return True


def is_pending(ret):
    return not ret["result"] is True or ret["changes"]


def is_same_result(run1, run2):
    for tag in run1:
        if (
            run2[tag]
            and run1[tag]["result"] == run2[tag]["result"]
            and run1[tag]["changes"] == run2[tag]["changes"]
        ):
            continue
        else:
            return False
    return True


def populate_wait_times(hub, runs):
    # Populate sleep times per state
    for tag in runs:
        state = tag_2_state(tag)
        if state not in _state_to_sleep_map.keys():
            _state_to_sleep_map[state] = getattr(
                hub.states[state],
                "__reconcile_wait__",
                {"static": {"wait_in_seconds": DEFAULT_RECONCILE_WAIT}},
            )


def get_max_wait_time(hub, runs, run_count):
    max_sleep_time = DEFAULT_RECONCILE_WAIT
    for tag in runs:
        if is_pending(runs[tag]):
            state_wait = _state_to_sleep_map[tag_2_state(tag)]
            wait_alg = list(state_wait.keys())[0]
            wait_val = state_wait[wait_alg]
            sleep_time = hub.reconcile.wait[wait_alg].get(
                **wait_val, run_count=run_count
            )
            if sleep_time > max_sleep_time:
                max_sleep_time = sleep_time

    return max_sleep_time


def populate_old_states(run):
    # Keep old_state per tag from the original run
    tag_to_old_state = {}
    for tag in run:
        if run[tag].get("old_state", None):
            tag_to_old_state[tag] = copy.deepcopy(run[tag]["old_state"])
    return tag_to_old_state


def update_changes(hub, last_run, tag_to_old_state_map):
    # Update last_run with 'old_state' from the original run
    # and recalculate last_run 'changes' to reflect
    # all the changes that occurred during reconciliation:
    # the delta between original run's old_state and last_run 'new_state'
    for tag in last_run:
        orig_old_state = tag_to_old_state_map.get(tag, None)
        last_old_state = last_run[tag].get("old_state", None)
        if orig_old_state != last_old_state:
            hub.log.debug(
                f"Replacing 'old_state' for '{tag_2_state(tag)}': {last_old_state} with {orig_old_state}"
            )

        last_run[tag]["old_state"] = orig_old_state
        last_run[tag]["changes"] = differ.deep_diff(
            orig_old_state if orig_old_state else dict(),
            last_run[tag].get("new_state", dict()),
        )


def tag_2_state(tag):
    # Get state from the tag
    return tag[0 : tag.find("_|")]
