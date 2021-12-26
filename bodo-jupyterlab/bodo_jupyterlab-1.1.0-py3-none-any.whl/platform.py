from requests.models import Response
from .config import (
    AUTH_API,
    BACKEND_API,
    NOTEBOOK_UUID,
    BACKEND_API_ACCESS_TOKEN_LOC,
    BACKEND_API_REFRESH_TOKEN_LOC,
    GET_CLUSTER_LIST_REFRESH_PERIOD_SECONDS,
    GET_CLUSTER_INFO_REFRESH_PERIOD_SECONDS,
    GET_CLUSTER_INFO_MAX_CACHE_SIZE,
    GET_CLUSTER_INFO_MAX_RETRIES,
    GET_CLUSTER_LIST_MAX_RETRIES,
)
import requests
import json
from cachetools import TTLCache, cached
from cachetools.keys import hashkey


class PlatformTokensManager:

    access_token: str = ""
    refresh_token: str = ""

    @classmethod
    def get_access_token(cls) -> str:
        if not cls.access_token:
            cls._load_tokens_from_disk()
        return cls.access_token

    @classmethod
    def get_refresh_token(cls) -> str:
        if not cls.refresh_token:
            cls._load_tokens_from_disk()
        return cls.refresh_token

    @classmethod
    def _load_tokens_from_disk(cls):
        try:
            with open(BACKEND_API_ACCESS_TOKEN_LOC, "r") as f:
                cls.access_token = f.read().strip()
            with open(BACKEND_API_REFRESH_TOKEN_LOC, "r") as f:
                cls.refresh_token = f.read().strip()
        except Exception as e:
            print("Error getting tokens from disk: ", e)
            raise

    @classmethod
    def _write_tokens_to_disk(cls):
        try:
            if cls.access_token and cls.refresh_token:
                with open(BACKEND_API_ACCESS_TOKEN_LOC, "w") as f:
                    f.write(cls.access_token)
                with open(BACKEND_API_REFRESH_TOKEN_LOC, "w") as f:
                    f.write(cls.refresh_token)
        except Exception as e:
            print("Error writing tokens to disk: ", e)
            raise

    @classmethod
    def refresh_tokens(cls):
        res: Response = requests.get(
            f"{AUTH_API}/auth/refresh",
            headers={"Authorization": f"Bearer {cls.refresh_token}"},
        )

        if not res.ok:
            raise Exception(f"Unable to refresh tokens. Response: {res}")

        data = json.loads(res.content.decode("utf-8"))
        cls.access_token = data["access_token"]
        cls.refresh_token = data["refresh_token"]
        cls._write_tokens_to_disk()


class PlatformClusterManager:

    # Keep in sync with ICluster interface in src/types.ts
    CLUSTER_FIELDS = [
        "uuid",
        "name",
        "workersQuantity",
        "instanceType",
        "status",
        "bodoVersion",
    ]

    @classmethod
    def _get_clusters_list(cls) -> Response:
        access_token = PlatformTokensManager.get_access_token()
        res: Response = requests.get(
            f"{BACKEND_API}/cluster?withTasks=false&clusterSource=user",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        return res

    @staticmethod
    def tokens_needs_to_be_refreshed(res: Response) -> bool:
        return (not res.ok) and (res.status_code in (401, 403))

    @classmethod
    @cached(
        cache=TTLCache(maxsize=2, ttl=GET_CLUSTER_LIST_REFRESH_PERIOD_SECONDS),
        key=lambda cls, logger: hashkey("A"),
    )
    def get_clusters_list(cls, logger):
        logging_prefix = f"[GetClustersList]"
        try:
            logger.info(f"{logging_prefix} Calling Backend for clusters list...")
            res: Response = cls._get_clusters_list()

            num_retries = 0
            while (
                PlatformClusterManager.tokens_needs_to_be_refreshed(res)
                and num_retries < GET_CLUSTER_LIST_MAX_RETRIES
            ):
                logger.info(f"{logging_prefix} Refreshing tokens...")
                PlatformTokensManager.refresh_tokens()
                res = cls._get_clusters_list()
                num_retries += 1

            if not res.ok:
                e = f"Could not get cluster list from platform! Response: {res}"
                logger.info(f"{logging_prefix} ERROR: {e}")
                raise Exception(e)

            logger.info(f"{logging_prefix} Response: {res}")
            clusters = json.loads(res.content.decode("utf-8"))
            clusters = list(filter(lambda x: x["status"] == "RUNNING", clusters))
            logger.info(
                f"{logging_prefix} Cluster list received from backend: {clusters}"
            )
            # Only keep the required fields
            clusters = [
                {FIELD: c.get(FIELD) for FIELD in cls.CLUSTER_FIELDS} for c in clusters
            ]
            logger.info(f"{logging_prefix} Clusters (after filtering): {clusters}")
            return clusters

        except Exception as e:
            logger.error(
                f"{logging_prefix} Error in PlatformClusterManager.get_clusters_list: {e}"
            )
            raise

    @classmethod
    def _get_cluster_info(cls, cluster_uuid: str) -> Response:
        access_token = PlatformTokensManager.get_access_token()
        query = f"?notebookUUID={NOTEBOOK_UUID}" if NOTEBOOK_UUID else ""
        res = requests.get(
            f"{BACKEND_API}/cluster/{cluster_uuid}/connection-info{query}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        return res

    @classmethod
    @cached(
        cache=TTLCache(
            maxsize=GET_CLUSTER_INFO_MAX_CACHE_SIZE,
            ttl=GET_CLUSTER_INFO_REFRESH_PERIOD_SECONDS,
        ),
        key=lambda cls, cluster_uuid, logger: hashkey(cluster_uuid),
    )
    def get_cluster_info(cls, cluster_uuid: str, logger):
        logging_prefix = f"[GetClusterInfo][UUID: {cluster_uuid}]"
        try:
            logger.info(
                f"{logging_prefix} Getting cluster info for cluster_uuid: {cluster_uuid}"
            )
            res = cls._get_cluster_info(cluster_uuid)

            num_retries = 0
            while (
                PlatformClusterManager.tokens_needs_to_be_refreshed(res)
                and num_retries < GET_CLUSTER_INFO_MAX_RETRIES
            ):
                PlatformTokensManager.refresh_tokens()
                res = cls._get_cluster_info(cluster_uuid)
                num_retries += 1

            if not res.ok:
                e = "ERROR: Could not get cluster infor from platform! Got non-ok response"
                logger.error(f"{logging_prefix} {e}")
                raise Exception(e)

            cluster_info = json.loads(res.content.decode("utf-8"))
            logger.info(
                f"{logging_prefix} Cluster Info received from backend: {cluster_info}"
            )
            return cluster_info

        except Exception as e:
            logger.error(
                f"{logging_prefix} Error in PlatformClusterManager.get_cluster_info: {e}"
            )
            raise

    @classmethod
    def get_cluster_hostlist(cls, cluster_uuid: str, logger):
        return cls.get_cluster_info(cluster_uuid, logger)["hostList"]
