import uuid

import pytest
from squall_router import Router


VALIDATORS = [
    ("int", "^[0-9]+$"),
    ("float", "^[0-9]+(.[0-9]+)?$"),
    ("uuid", "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"),
]


ROUTES = [
    # METHOD, PATH, HANDLER_ID, PARAMS_MATCH
    ("GET", "/authorizations", 0, {}),
    ("GET", "/authorizations/{param1}", 1, {"param1": "auth"}),
    ("GET", "/repos/{param1}/{param2}/subscription", 2, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/events", 3, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/notifications", 4, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/stargazers", 5, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/subscribers", 6, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/issues", 7, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/issues/{param3}", 8, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/repos/{param1}/{param2}/assignees", 9, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/assignees/{param3}", 10, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/repos/{param1}/{param2}/issues/{param3}/comments", 11, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/repos/{param1}/{param2}/issues/{param3}/events", 12, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/repos/{param1}/{param2}/labels", 13, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/labels/{param3}", 14, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/repos/{param1}/{param2}/issues/{param3}/labels", 15, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/repos/{param1}/{param2}/milestones/{param3}/labels", 16, {"param1": "1", "param2": "22", "param3": "33"}),
    ("GET", "/repos/{param1}/{param2}/milestones/", 17, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/milestones/{param3}", 18, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/repos/{param1}/{param2}/git/blobs/{param3}", 19, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/repos/{param1}/{param2}/git/commits/{param3}", 20, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/repos/{param1}/{param2}/git/refs", 21, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/git/tags/{param3}", 22, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/repos/{param1}/{param2}/git/trees/{param3}", 23, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/repos/{param1}/{param2}/pulls", 24, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/pulls/{param3}", 25, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/repos/{param1}/{param2}/pulls/{param3}/commits", 26, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/repos/{param1}/{param2}/pulls/{param3}/files", 27, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/repos/{param1}/{param2}/pulls/{param3}/merge", 28, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/repos/{param1}/{param2}/pulls/{param3}/comments", 29, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/repos/{param1}/{param2}", 30, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/contributors", 31, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/languages", 32, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/teams", 33, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/tags", 34, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/branches", 35, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/branches/{param3}", 36, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/repos/{param1}/{param2}/collaborators", 37, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/collaborators/{param3}", 38, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/repos/{param1}/{param2}/comments", 39, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/commits/{param3}/comments", 40, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/repos/{param1}/{param2}/commits", 41, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/commits/{param3}", 42, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/repos/{param1}/{param2}/readme", 43, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/keys", 44, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/keys/{param3}", 45, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/repos/{param1}/{param2}/downloads", 46, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/downloads/{param3}", 47, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/repos/{param1}/{param2}/forks", 48, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/hooks", 49, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/hooks/{param3}", 50, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/repos/{param1}/{param2}/releases", 51, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/releases/{param3}", 52, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/repos/{param1}/{param2}/releases/{param3}/assets", 53, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/repos/{param1}/{param2}/stats/contributors", 54, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/stats/commit_activity", 55, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/stats/code_frequency", 56, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/stats/participation", 57, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/stats/punch_card", 58, {"param1": "123", "param2": "321"}),
    ("GET", "/repos/{param1}/{param2}/statuses/{param3}", 59, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/users/{param1:int}/received_events", 60, {"param1": "123"}),
    ("GET", "/users/{param1:int}/received_events/public", 61, {"param1": "123"}),
    ("GET", "/users/{param1:int}/events", 62, {"param1": "123"}),
    ("GET", "/users/{param1:int}/events/public", 63, {"param1": "123"}),
    ("GET", "/users/{param1:int}/events/orgs/{param2}", 64, {"param1": "123", "param2": "22"}),
    ("GET", "/users/{param1}/starred", 65, {"param1": "123"}),
    ("GET", "/user/starred", 66, {}),
    ("GET", "/user/starred/{param1}/{param2}", 67, {"param1": "123", "param2": "321"}),
    ("GET", "/users/{param1}/subscriptions", 68, {"param1": "123"}),
    ("GET", "/user/subscriptions", 69, {}),
    ("GET", "/user/subscriptions/{param1}/{param2}", 70, {"param1": "123", "param2": "321"}),
    ("GET", "/users/{param1}", 71, {"param1": "123"}),
    ("GET", "/user", 72, {}),
    ("GET", "/users", 73, {}),
    ("GET", "/user/emails", 74, {}),
    ("GET", "/users/{param1}/followers", 75, {"param1": "123"}),
    ("GET", "/user/followers", 76, {}),
    ("GET", "/users/{param1}/following", 77, {"param1": "123"}),
    ("GET", "/user/following", 78, {}),
    ("GET", "/user/following/{param1}", 79, {"param1": "123"}),
    ("GET", "/users/{param1}/following/{param2}", 80, {"param1": "123", "param2": "22"}),
    ("GET", "/users/{param1}/keys", 81, {"param1": "123"}),
    ("GET", "/user/keys", 82, {}),
    ("GET", "/user/keys/{param1}", 83, {"param1": "123"}),
    ("GET", "/user/teams", 84, {}),
    ("GET", "/user/repos", 85, {}),
    ("GET", "/users/{param1}/repos", 86, {"param1": "123"}),
    ("GET", "/users/{param1}/orgs", 87, {"param1": "123"}),
    ("GET", "/user/orgs", 88, {}),
    ("GET", "/users/{param1}/gists", 89, {"param1": "123"}),
    ("GET", "/user/issues", 90, {}),
    ("GET", "/networks/{param1:int}/{param2:int}/events", 91, {"param1": "123", "param2": "321"}),
    ("GET", "/networks/{param1:int}/{param2:uuid}/events", 92, {"param1": "123", "param2": str(uuid.uuid4())}),
    ("GET", "/feeds", 93, {}),
    ("GET", "/notifications", 94, {}),
    ("GET", "/notifications/threads/{param1}", 95, {"param1": "123"}),
    ("GET", "/notifications/threads/{param1}/subscription", 96, {"param1": "123"}),
    ("GET", "/gists", 97, {}),
    ("GET", "/gists/{param1}", 98, {"param1": "123"}),
    ("GET", "/gists/{param1}/star", 99, {"param1": "123"}),
    ("GET", "/issues", 100, {}),
    ("GET", "/orgs/{param1}/issues", 101, {"param1": "123"}),
    ("GET", "/gitignore/templates", 102, {}),
    ("GET", "/gitignore/templates/{param1}", 103, {"param1": "123"}),
    ("GET", "/orgs/{param1}", 104, {"param1": "123"}),
    ("GET", "/orgs/{param1}/members", 105, {"param1": "123"}),
    ("GET", "/orgs/{param1}/members/{param2}", 106, {"param1": "123", "param2": "321"}),
    ("GET", "/orgs/{param1}/public_members", 107, {"param1": "123"}),
    ("GET", "/orgs/{param1}/public_members/{param2}", 108, {"param1": "123", "param2": "321"}),
    ("GET", "/orgs/{param1}/teams", 109, {"param1": "123"}),
    ("GET", "/orgs/{param1}/events", 110, {"param1": "123"}),
    ("GET", "/orgs/{param1}/repos", 111, {"param1": "123"}),
    ("GET", "/teams/{param1}", 112, {"param1": "123"}),
    ("GET", "/teams/{param1}/members", 113, {"param1": "123"}),
    ("GET", "/teams/{param1}/members/{param2}", 114, {"param1": "123", "param2": "321"}),
    ("GET", "/teams/{param1}/repos", 115, {"param1": "123"}),
    ("GET", "/teams/{param1}/repos/{param2}/{param3}", 116, {"param1": "11", "param2": "22", "param3": "33"}),
    ("GET", "/search/repositories", 117, {}),
    ("GET", "/search/code", 118, {}),
    ("GET", "/search/issues", 119, {}),
    ("GET", "/search/users", 120, {}),
    ("GET", "/applications/{param1}/tokens/{param2:uuid}", 121, {"param1": "123", "param2": str(uuid.uuid4())}),
    ("GET", "/events", 122, {}),
    ("GET", "/emojis", 123, {}),
    ("GET", "/meta", 124, {}),
    ("GET", "/rate_limit", 125, {}),
    ("GET", "/repositories", 126, {}),
    ("GET", "/legacy/issues/search/{param1}/{param2}/{param3}/{param4}", 127, {"param1": "11", "param2": "22", "param3": "33", "param4": "44"}),
    ("GET", "/legacy/repos/search/{param1}", 128, {"param1": "123"}),
    ("GET", "/legacy/user/search/{param1}", 129, {"param1": "123"}),
    ("GET", "/legacy/user/email/{param1}", 130, {"param1": "123"}),
]

LOCATIONS = [
    ("GET", "/static/css", 201),
    ("GET", "/static/js", 202),
    ("GET", "/static/img", 203),
]


@pytest.fixture(scope="session")
def router():
    router = Router()
    for validator, pattern in VALIDATORS:
        router.add_validator(validator, pattern)

    for method, path, handler_id, _ in ROUTES:
        try:
            router.add_route(method, path, handler_id)
        except ValueError:
            raise ValueError(method, path, handler_id)

    for method, location, handler_id in LOCATIONS:
        router.add_route(method, location, handler_id)

    return router


@pytest.mark.parametrize(
    "method,path,expected_handler,expected_params",
    [(i[0], i[1], i[2], i[3]) for i in ROUTES]
)
def test_resolve(router, method, path, expected_handler, expected_params):
    request_path = (
        path.replace(":int", "")
            .replace(":uuid", "")
            .replace(":float", "")
            .format(**expected_params)
    )

    handler_id, params = router.resolve(method, request_path)
    assert handler_id == expected_handler
    assert dict(params) == expected_params


@pytest.mark.parametrize(
    "path,expected_handler,expected_params",
    [(i[1], i[2], i[3]) for i in ROUTES]
)
def test_resolve_not_found(router, path, expected_handler, expected_params):
    request_path = (
        path.replace(":int", "")
            .replace(":uuid", "")
            .replace(":float", "")
            .format(**expected_params)
    )
    assert router.resolve("POST", request_path) is None


@pytest.mark.parametrize(
    "method,path,expected_handler,expected_params",
    [(i[0], i[1], i[2], i[3]) for i in ROUTES if ":int" in i[1]]
)
def test_pass_string_to_int_validated_fields(router, method, path, expected_handler, expected_params):
    not_applicable_params = {k: "non_int" for k in expected_params}
    request_path = path.replace(":int", "").replace(":uuid", "").format(**not_applicable_params)
    assert router.resolve("POST", request_path) is None
