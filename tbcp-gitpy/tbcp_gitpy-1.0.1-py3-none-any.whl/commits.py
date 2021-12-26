"""
Working with Git Commits object

Reference:
- https://gitpython.readthedocs.io/en/stable/tutorial.html#the-commit-object
- https://gitpython.readthedocs.io/en/stable/tutorial.html#understanding-objects
"""

import sys
import git
from .repository import Repository


class Commits(Repository):
    """Inherits the self.repo instance"""

    def set_commit(message):
        try:
            repo = super().get_repo()
            repo.git.commit(m=message)
        except git.InvalidGitRepositoryError as error:
            print(f"Oops! That was not a valid Git repository {format(error)}")
            raise
        except git.GitCommandError as error:
            print(f"Oops! That was not a valid Git command {format(error)}")
            raise
        except ValueError:
            print(f"That is not a string. Try again!: {format(sys.exc_info()[0])}")
            raise
        except BaseException:
            print(f"Unexpected error: {format(sys.exc_info()[0])}")
            raise

    def commit_to_dict(self, commit):
        """Convert given Commit Instance in structered Object"""
        return {
            "hexsha": str(commit.hexsha),
            "tree": {"type": str(commit.tree.type)},
            "summary": str(commit.summary),
            "message": str(commit.message),
            "parents": commit.parents,
            "author": {"name": str(commit.author.name), "email": str(commit.author.email)},
            "committer": {
                "name": str(commit.committer.name),
                "email": str(commit.committer.email),
            },
            "authored_datetime": str(commit.authored_datetime),
            "authored_date": int(commit.authored_date),
            "committed_date": int(commit.committed_date),
            "count": int(commit.count()),
            "size": int(commit.size),
        }

    def get_recent_commit(self) -> dict:
        """Return the latest commit of the repository"""
        repo = super().get_repo()
        return self.commit_to_dict(repo.head.commit)

    def get_list_of_commits(self, head="main", max_count=50, skip=0) -> list:
        repo = super().get_repo()

        list_of_commits = []
        for commit in repo.iter_commits(head, max_count=max_count, skip=skip):
            list_of_commits.append(self.commit_to_dict(commit))

        return list_of_commits

    def get_commit_by_hexsha(self, hexsha: str):
        """
        Provide a list of commits. Default: max=50, head=main, skip=0

        - commit.hexsha
        - commit.summary
        - commit.author.name
        - commit.author.email
        - commit.authored_datetime
        - commit.count()
        - commit.size
        """

        commit_of_hexsha = ""
        list_of_commits = self.get_list_of_commits()
        for commit in list_of_commits:
            if hexsha == commit["hexsha"]:
                commit_of_hexsha = commit

        return commit_of_hexsha


#     def catch_commit_from_hook(self, repo_instance):
#         """Catch a commit message"""
#         self.repo_instance = repo_instance

#         self.repo_instance.index.commit('Initial commit.')

#     def take_commit_message(self, repo_instance, commit_message):
#         """Provide a commit message"""
#         self.repo_instance = repo_instance
#         self.commit_message = commit_message

#         self.repo_instance.index.commit('Initial commit.')
