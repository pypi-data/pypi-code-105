from ..retrieve_holder import RetrieveHolder
from ..utils import Utils


class Ingest:
    def __init__(self, stub, feature_set, ingest):
        self._stub = stub
        self._feature_set = feature_set
        self._ingest = ingest

    def retrieve(self):
        if self._ingest.ingest_id == "-1":
            raise NotImplementedError(
                "Data ingested before system version 0.0.36 is not supported for retrieval via this API."
            )
        return RetrieveHolder(
            self._stub, self._feature_set, "", "", self._ingest.ingest_id
        )

    def __repr__(self):
        return Utils.pretty_print_proto(self._ingest)
