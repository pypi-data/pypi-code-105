#
from pkg_resources import parse_version
import requests
import six
import wandb


def _find_available(current_version):
    pypi_url = "https://pypi.org/pypi/%s/json" % wandb._wandb_module

    yanked_dict = {}
    try:
        async_requests_get = wandb.util.async_call(requests.get, timeout=5)
        data, thread = async_requests_get(pypi_url, timeout=3)
        if not data or isinstance(data, Exception):
            return
        data = data.json()
        latest_version = data["info"]["version"]
        release_list = data["releases"].keys()
        for version, fields in six.iteritems(data["releases"]):
            for item in fields:
                yanked = item.get("yanked")
                yanked_reason = item.get("yanked_reason")
                if yanked:
                    yanked_dict[version] = yanked_reason
    except Exception:
        # Any issues whatsoever, just skip the latest version check.
        return

    # Return if no update is available
    pip_prerelease = False
    deleted = False
    yanked = False
    yanked_reason = None
    parsed_current_version = parse_version(current_version)

    # Check if current version has been yanked or deleted
    # NOTE: we will not return yanked or deleted if there is nothing to upgrade to
    if current_version in release_list:
        yanked = current_version in yanked_dict
        yanked_reason = yanked_dict.get(current_version)
    else:
        deleted = True

    # Check pre-releases
    if parse_version(latest_version) <= parsed_current_version:
        # pre-releases are not included in latest_version
        # so if we are currently running a pre-release we check more
        if not parsed_current_version.is_prerelease:
            return
        # Candidates are pre-releases with the same base_version
        release_list = map(parse_version, release_list)
        release_list = filter(lambda v: v.is_prerelease, release_list)
        release_list = filter(
            lambda v: v.base_version == parsed_current_version.base_version,
            release_list,
        )
        release_list = sorted(release_list)
        if not release_list:
            return

        parsed_latest_version = release_list[-1]
        if parsed_latest_version <= parsed_current_version:
            return
        latest_version = str(parsed_latest_version)
        pip_prerelease = True

    return latest_version, pip_prerelease, deleted, yanked, yanked_reason


def check_available(current_version):
    package_info = _find_available(current_version)
    if not package_info:
        return

    latest_version, pip_prerelease, deleted, yanked, yanked_reason = package_info
    upgrade_message = (
        "%s version %s is available!  To upgrade, please run:\n"
        " $ pip install %s --upgrade%s"
        % (
            wandb._wandb_module,
            latest_version,
            wandb._wandb_module,
            " --pre" if pip_prerelease else "",
        )
    )

    delete_message = None
    if deleted:
        delete_message = "%s version %s has been retired!  Please upgrade." % (
            wandb._wandb_module,
            current_version,
        )
    yank_message = None
    if yanked:
        reason_message = "(%s)  " % yanked_reason if yanked_reason else ""
        yank_message = "%s version %s has been recalled!  %sPlease upgrade." % (
            wandb._wandb_module,
            current_version,
            reason_message,
        )

    # A new version is available!
    return {
        "upgrade_message": upgrade_message,
        "yank_message": yank_message,
        "delete_message": delete_message,
    }
