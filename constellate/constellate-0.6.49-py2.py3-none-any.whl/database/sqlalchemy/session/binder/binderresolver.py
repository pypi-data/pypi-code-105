from typing import List, Any
from sqlalchemy.exc import UnboundExecutionError

from constellate.database.sqlalchemy.sqlalchemydbconfig import SQLAlchemyDBConfig


class BinderResolver:
    def __init__(self, resolvers: List[Any] = None, default_config: SQLAlchemyDBConfig = None):
        self._resolvers = resolvers
        self._default_config = default_config

    def get_bind(
        self,
        mapper=None,
        clause=None,
        bind=None,
        _sa_skip_events=None,
        _sa_skip_for_implicit_returning=False,
    ):
        # clause = SELECT * FROM ....
        # mapper = Class being used to access a table. Eg: TradeR

        # Try custom resolvers
        count = len(self._resolvers)
        for index, resolver in enumerate(self._resolvers):
            try:
                _bind = resolver.get_bind(
                    mapper=mapper,
                    clause=clause,
                    bind=bind,
                    _sa_skip_events=_sa_skip_events,
                    _sa_skip_for_implicit_returning=_sa_skip_for_implicit_returning,
                )
                if _bind is not None:
                    return _bind
            except UnboundExecutionError as e:
                if index + 1 == count:
                    # Last resolver did not find any bind
                    if self._default_config is not None:
                        # Use default config as bind when present
                        return self._default_config.engine_config.sync_engine
                    raise e
                else:
                    continue

        return UnboundExecutionError()
