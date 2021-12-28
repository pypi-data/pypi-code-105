import os

SUPPORT_LOCAL_CACHE = False
SUPPORT_MEM_CACHE = False

ENABLE_SET_CACHE_WHEN_GET = False

if os.getenv("CLUSTER_NAME", "not online") in ["c5"]:
    THETIS_HTTP_ENDPOINT = "thetis.c5-cloudml.xiaomi.srv"
else:
    #THETIS_HTTP_ENDPOINT = "thetis.c5-staging-cloudml.xiaomi.srv"
    THETIS_HTTP_ENDPOINT = "dushulin.thetis.c5-cloudml-staging.xiaomi.srv"

LOCAL_CACHE_ROOT_PATH = os.getenv("LOCAL_CACHE_ROOT_PATH", "/tmp/cloudml") 

MEM_CACHE_ROOT_PATH = os.getenv("MEM_CACHE_ROOT_PATH", "/dev/shm/cloudml")