from abc import ABC, abstractmethod

from cloudml.adrn_parser import get_dataset_name_version_from_adrn
from cloudml.dataset_srv_stub import StubBase, gen_visit_stub_from_adrn
from cloudml.item_handler import BaseItemHandler, ItemHandlerGenerator, FileCacheType
from cloudml import settings


class BaseAdrnDataSet(ABC):

    @abstractmethod
    def item_list(self):
        return []

    @abstractmethod
    def handler_list(self) -> BaseItemHandler:
        return []

    @abstractmethod
    def parse_path(self, item): 
        return None

    @abstractmethod
    def parse_label(self, item):
        return None   

    def get_label_and_content(self, idx):
        if len(self.item_list()) <= 0:
            raise Exception("the length of dataset is 0 !")
        item = self.item_list()[idx]
        label = self.parse_label(item)
        rpath = self.parse_path(item)
        img = None
        for hdr in self.handler_list():
            content = hdr.get_data(rpath)
            if content:
                img = content
                break    
        return label, img


class ThetisAdrnDataSet(BaseAdrnDataSet):

    def __init__(self, adrn, visit_stub : StubBase):
        self._visit_stub = visit_stub
        srv_name, dataset_name,dataset_version = get_dataset_name_version_from_adrn(adrn)
        if srv_name != "data-set":
            raise Exception("service name: {} not support in AdrnDataSet!".format(srv_name))
        self._item_list = self._visit_stub.get_item_list(dataset_name, dataset_version)
        if len(self._item_list) <= 0:
            raise Exception("failed when get item list from the dataset!")
        prefix = self._visit_stub.parse_prefix_from_item(self._item_list[0])
        basic_handler = ItemHandlerGenerator.gen_from_item_prefix(prefix)
        self._handler_list = [basic_handler]
        if settings.SUPPORT_LOCAL_CACHE:
            handler = ItemHandlerGenerator.gen_for_file_cache(dataset_name,dataset_version, FileCacheType.localfs)
            self._handler_list.insert(0, handler)
        if settings.SUPPORT_MEM_CACHE:
            handler = ItemHandlerGenerator.gen_for_file_cache(dataset_name,dataset_version, FileCacheType.memfs)
            self._handler_list.insert(0, handler)

    def item_list(self):
        return self._item_list

    def handler_list(self):
        return self._handler_list

    def parse_path(self, item): 
        return self._visit_stub.parse_path_from_item(item)

    def parse_label(self, item):
        return self._visit_stub.parse_label_from_item(item)