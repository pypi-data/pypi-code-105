from glapi import configuration
from glapi.connection import GitlabConnection

class GitlabGroup:
    """
    GitlabGroup is a Gitlab Group.
    """

    def __init__(self, id: str = None, group: dict = None, token :str = configuration.GITLAB_TOKEN, version: str = configuration.GITLAB_API_VERSION):
        """
        Args:
            id (string): GitLab Project id
            group (dictionary): GitLab Group
            token (string): GitLab personal access or deploy token
            version (string): GitLab API version as base url
        """
        self.connection = GitlabConnection(
            token=token,
            version=version
        )
        self.group = group if group else (self.connection.query("groups/%s" % id)["data"] if id and token and version else None)
        self.id = self.group["id"] if self.group else None

    def extract_epics(self, date_start: str =  configuration.DATE_START, date_end: str =  configuration.DATE_END) -> list:
        """
        Extract group-specific epic data.

        Args:
            date_end (string): iso 8601 date value
            date_start (string): iso 8601 date value

        Returns:
            A list of dictionaries where each represents a GitLab Epic.
        """

        result = None

        params = {
            "created_after": date_start,
            "created_before": date_end
        }

        # check connection params
        if self.id and self.connection.token and self.connection.version:

            # query api for issues
            result = self.connection.paginate(
                endpoint="groups/%s/issues" % self.id,
                params=params
            )

        return result

    def extract_issues(self, scope: str = "all", date_start: str =  configuration.DATE_START, date_end: str =  configuration.DATE_END) -> list:
        """
        Extract group-specific issue data.

        Args:
            date_end (string): iso 8601 date value
            date_start (string): iso 8601 date value
            scope (enum): all | assigned_to_me | created_by_me

        Returns:
            A list of dictionaries where each represents a GtiLab Issue.
        """

        result = None

        params = {
            "created_after": date_start,
            "created_before": date_end,
            "scope": scope
        }

        # check connection params
        if self.id and self.connection.token and self.connection.version:

            # query api for issues
            result = self.connection.paginate(
                endpoint="groups/%s/issues" % self.id,
                params=params
            )

        return result
