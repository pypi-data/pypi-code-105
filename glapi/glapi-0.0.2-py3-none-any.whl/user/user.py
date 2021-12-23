from glapi import configuration
from glapi.connection import GitlabConnection

class GitlabUser:
    """
    GitlabUser is a GitLab User.
    """

    def __init__(self, id: str = None, username: str = None, user: dict = None, token :str = configuration.GITLAB_TOKEN, version: str = configuration.GITLAB_API_VERSION):
        """
        Args:
            id (string): GitLab User id
            token (string): GitLab personal access or deploy token
            user (dict): key/values representing a Gitlab User
            version (string): GitLab API version as base url
        """

        self.id = id
        self.connection = GitlabConnection(
            token=token,
            version=version
        )
        self.user = user

        # no user data provided
        if self.user is None:

            # prefer id query over username
            if self.id:

                # query by id
                self.user = self.connection.query("users/%s" % self.id)["data"]

            elif username:

                # query by username
                user_data = self.connection.query("users", params={ "username": username })["data"]
                self.user = user_data[0] if len(user_data) > 0 else dict()

    def extract_events(self, actions: list, date_start: str =  configuration.DATE_START, date_end: str =  configuration.DATE_END) -> dict:
        """
        Extract user-specific event data.

        Args:
            actions (list): enums where each represent an event action type https://docs.gitlab.com/ee/user/index.html#user-contribution-events
            date_end (string): iso 8601 date value
            date_start (string): iso 8601 date value

        Returns:
            A dictionary where keys are event action types and corresponding values are lists of dictionaries where each represents a GitLab Event.
        """

        result = None

        # check for connection ready
        if self.id and self.connection.token and self.connection.version:

            # update result
            result = dict()

            # loop through actions
            for action in actions:

                # get events
                result[action] = self.connection.paginate(
                    endpoint="users/%s/events" % self.id,
                    params={
                        "action": action,
                        "after": date_start,
                        "before": date_end
                    }
                )

        return result

    def extract_issues(self, scope: str, date_start: str =  configuration.DATE_START, date_end: str =  configuration.DATE_END) -> list:
        """
        Extract user-specific issue data.

        Args:
            date_end (string): iso 8601 date value
            date_start (string): iso 8601 date value
            scope (enum): "assigned_to_me" | "created_by_me"

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
                endpoint="issues",
                params=params
            )

        return result

    def extract_merge_requests(self, scope: str, date_start: str =  configuration.DATE_START, date_end: str =  configuration.DATE_END) -> list:
        """
        Extract user-specific merge request data.

        Args:
            date_end (string): iso 8601 date value
            date_start (string): iso 8601 date value
            scope (enum): "assigned_to_me" | "created_by_me"

        Returns:
            A list of dictionaries where each represents a GtiLab MergeRequest.
        """

        result = None

        params = {
            "created_after": date_start,
            "created_before": date_end
        }

        if scope:

            # update params
            params["scope"] = scope

        # check for connection params
        if self.id and self.connection.token and self.connection.version:

            # query api for issues
            result = self.connection.paginate(
                endpoint="merge_requests",
                params=params
            )

        return result

    def extract_projects(self, access: int = configuration.GITLAB_PROJECT_USER_ACCESS, simple: bool = configuration.GITLAB_PROJECT_SIMPLE, visibility: str = configuration.GITLAB_PROJECT_VISIBILITY, personal: bool = configuration.GITLAB_PROJECT_PERSONAL_ONLY, membership: bool = configuration.GITLAB_PROJECT_USER_MEMBERSHIP) -> list:
        """
        Extract user-specific project data.

        Args:
            access (integer): minimum access level of a user on a given project
            membership (boolean): TRUE if api should query specific to the user attached to the access token
            personal (boolean): TRUE if api should return namespace (personal) user projects only
            simple (boolean): TRUE if api return should be minimal
            visibility (enum): internal | private | public

        Returns:
            A list of dictionaries where each represents a Gitlab Project.
        """

        result = None

        # check connection params
        if self.id and self.connection.token and self.connection.version:

            if personal:

                # namespace projects
                result = self.connection.paginate(
                    endpoint="users/%s/projects" % self.id,
                    params={
                        "simple": simple,
                        "visibility": visibility
                    }
                )

            else:

                # all projects
                result = self.connection.paginate(
                    endpoint="projects",
                    params={
                        "membership": membership,
                        "min_access_level": access,
                        "simple": simple,
                        "visibility": visibility
                    }
                )

        return result
