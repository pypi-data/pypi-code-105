from typing import Final

ERROR_SERVER_FAILURE: Final = "server error on {user}:{query}:{response}"
ERROR_SERVER_EMPTY: Final = "server empty response on {user}:{query}:{response}"
ERROR_LOGIN_AUTH: Final = "wrong credentials for {user}"
ERROR_CUPS: Final = "cups {cups} not found at server, available are: {cups_list}"