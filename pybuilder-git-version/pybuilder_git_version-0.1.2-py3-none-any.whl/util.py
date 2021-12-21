import re

import semver
from git import Repo
from pybuilder.core import Logger


class NoValidTagFoundError(Exception):
    pass


def find_latest_version_tag(repo: Repo, logger: Logger):
    valid_tags = [t for t in repo.tags if semver.VersionInfo.isvalid(t.name)]
    logger.debug("Valid tags are: %s", [t.name for t in valid_tags])
    if len(valid_tags) > 0:
        latest_tag = valid_tags[0]
        commits = list(repo.iter_commits(repo.active_branch))
        latest_tag_is_latest_commit = commits[0] == latest_tag.commit and repo.active_branch.name == 'master'
        on_master_branch = repo.active_branch.name == 'master'
        repo_dirty = repo.is_dirty()
        if latest_tag_is_latest_commit and on_master_branch and not repo_dirty:
            logger.info("Using unmodified tag %s", latest_tag)
            return latest_tag.name
        else:
            current_version = semver.bump_patch(latest_tag.name)
            distance = commits.index(latest_tag.commit)
            build_token = 'build' if on_master_branch else sane_branch_name(repo.active_branch.name)
            current_version = semver.replace(current_version, build=f"{build_token}.{distance}")
            return current_version
    else:
        logger.warn("No valid tags found")
        raise NoValidTagFoundError("No valid version tag found")


def sane_branch_name(branch_name):
    if '/' in branch_name:
        branch_part = branch_name.split('/')[-1]
    else:
        branch_part = branch_name
    return re.sub('[^a-z0-9]', '', branch_part.lower())
