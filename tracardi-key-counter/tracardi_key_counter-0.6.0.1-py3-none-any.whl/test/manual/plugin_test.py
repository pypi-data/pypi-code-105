from tracardi.domain.profile import Profile
from tracardi_plugin_sdk.service.plugin_runner import run_plugin

from tracardi_key_counter.plugin import KeyCounterAction

init = {
    "key": ['mobile', 'desktop', 'mobile'],
    'save_in': 'profile@stats.counters.MobileVisits'
}

payload = {}
profile = Profile(id="aaa")
result = run_plugin(KeyCounterAction, init, payload, profile)
print(result)
