"""
Working with Git Branches

- Listing branches
- Creating branches
- Switching branches

Refernences:
- https://gitpython.readthedocs.io/en/stable/tutorial.html#switching-branches
"""

from .repository import Repository
from .commits import Commits
from .files import Files


class Branches(Repository):
    """Inherits the self.repo instance"""

    def get_branch(self) -> str:
        """Return the active branch of the current repository"""
        repo = super().get_repo()
        return str(repo.active_branch)

    def list_branches(self) -> list:
        """List all branches of the local repository"""
        repo = super().get_repo()

        list_branches = []
        for branch in repo.branches:
            if branch:
                list_branches.append(format(branch))

        return list_branches

    def check_if_branch_exists(self, branch) -> bool:
        """Check if the given branch exists"""

        return bool(branch in self.list_branches())

    def create_branch(self, branch_name: str, checkout=True, from_branch="main"):
        """Return the active branch of the current repository"""
        repo = super().get_repo()

        if self.check_if_branch_exists(branch_name):
            head = repo.create_head(branch_name)

            if checkout:
                super().set_checkout(head)

            if from_branch == "main":
                pull_branch = repo.heads.main
            else:
                pull_branch = repo.heads[from_branch]

            super().set_pull(pull_branch)

        if repo.index.diff(None) or repo.untracked_files:

            file_instance = Files()
            file_instance.set_add("ALL")

            commit_instance = Commits()
            commit_instance.set_commit("Message")

            super().set_push(head)
