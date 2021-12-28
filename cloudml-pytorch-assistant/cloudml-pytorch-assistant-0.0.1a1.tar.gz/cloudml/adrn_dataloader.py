from cloudml import settings
from cloudml.adrn_parser import parse_adrn
from cloudml.dataset_srv_stub import ThetisHttpStub
from cloudml.item_handler import FileCacheType, ItemHandlerGenerator

# srv for adrn resource from Http service
class AdrnHttpSrv(object):
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance == None:
            stub = ThetisHttpStub(None)
            cls._instance = AdrnHttpSrv(stub)
        return cls._instance

    def __init__(self, visit_stub : ThetisHttpStub):
        self._visit_stub = visit_stub
        basic_handler = ItemHandlerGenerator.gen_from_item_prefix("http://cnbj1.fds.api.xiaomi.com/thetis")
        self._handler_list = [basic_handler]
        if settings.SUPPORT_LOCAL_CACHE:
            handler = ItemHandlerGenerator.gen_for_file_cache(None, None, FileCacheType.localfs)
            self._handler_list.insert(0, handler)
        if settings.SUPPORT_MEM_CACHE:
            handler = ItemHandlerGenerator.gen_for_file_cache(None,None, FileCacheType.memfs)
            self._handler_list.insert(0, handler)

    def get_file(self, project_name, res_name, res_version, index):
        item_data = self._visit_stub.get_item_file(project_name, res_name, res_version, index)
        rpath = self._visit_stub.parse_path_from_item(item_data)
        img = None
        for hdr in self._handler_list:
            content = hdr.get_data(rpath)
            if content:
                img = content
                break    
        return img


def get_res_from_adrn(adrn):
    srv = AdrnHttpSrv.get_instance()
    srv_name, project_name, res_name, _, res_version, index = parse_adrn(adrn)
    if srv_name == "data-file":
        return srv.get_file(project_name, res_name, res_version, index)
    else:
        raise Exception("res type: {} is not support!".format(srv_name))
    