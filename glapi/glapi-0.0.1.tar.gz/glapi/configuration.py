import os

# GITLAB
GITLAB_API_VERSION = os.environ["GITLAB_API_VERSION"] if "GITLAB_API_VERSION" in os.environ else "https://gitlab.com/api/v4"
GITLAB_PAGINATION_PER_PAGE = int(os.environ["GITLAB_PAGINATION_PER_PAGE"]) if "GITLAB_PAGINATION_PER_PAGE" in os.environ else 100
GITLAB_TOKEN = os.environ["GITLAB_TOKEN"] if "GITLAB_TOKEN" in os.environ else None
