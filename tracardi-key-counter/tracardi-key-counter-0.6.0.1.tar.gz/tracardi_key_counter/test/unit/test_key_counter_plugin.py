from tracardi.domain.profile import Profile
from tracardi_plugin_sdk.service.plugin_runner import run_plugin

from tracardi_key_counter.plugin import KeyCounterAction


def test_key_counter_plugin():
    init = {
        "key": ['mobile', 'desktop', 'mobile'],
        'save_in': 'profile@stats.counters.MobileVisits'
    }

    payload = {}
    profile = Profile(id="aaa")
    result = run_plugin(KeyCounterAction, init, payload, profile)
    assert result.output.value == {'mobile': 2, 'desktop': 1}
