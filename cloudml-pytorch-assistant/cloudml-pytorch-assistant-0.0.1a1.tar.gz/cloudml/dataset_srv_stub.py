import json
import requests

from abc import ABC, abstractmethod
from cloudml.adrn_parser import parse_adrn

from cloudml import settings


class StubBase(ABC):

    @abstractmethod
    def get_item_list(self, name, version):
        pass 

    @abstractmethod
    def parse_path_from_item(self, item):
        pass

    @abstractmethod
    def parse_prefix_from_item(self, item):
        pass

    @abstractmethod
    def parse_label_from_item(self, item):
        pass


# stub for Thetis dataset from Http service
class ThetisHttpStub(StubBase):
    def __init__(self, ownerid):
        self.ownerid = ownerid
        self.endpoint = settings.THETIS_HTTP_ENDPOINT

    def get_item_list(self, name, version):
        hash_list = self.get_hash_list(self.ownerid, name, version)
        item_list = []
        for h in hash_list:
            item = self.get_item_label(self.ownerid, name, version, h)
            if item:
                item_list.append(item)
        return item_list

    def parse_path_from_item(self, item):
        return item["fdsUrl"].split("/")[-1]

    def parse_prefix_from_item(self, item):
        dn = item["fdsUrl"].split("/")[:-1]
        return "http://" + '/'.join(dn)

    def parse_label_from_item(self, item):
        return ','.join(item["label"])

    def _get_digit_id(self, ownerid):
        digit_name = []
        for a  in ownerid:
            if a.isdigit():
                digit_name.append(a)
        project_name = ''.join(digit_name)
        return project_name

    '''
    获取hashList: 
    http://thetis.c5-cloudml.xiaomi.srv/image/getV2?datasetName=wttest3&version=1&ownerTeamId=3797
    response
    {
        "status":{
            "code": 200,
            "message": success
        },
        "data":{
            "dataItemList":["02abd6f300a0dbf1d0275d5d20684358db857638", "07cad1b02c72b63022acdb6a4cf9f0c224288c0e"]
        }
    }
    '''
    def get_hash_list(self, ownerid, name, version):
        ownerid = self._get_digit_id(ownerid)
        uri = "http://" + self.endpoint + "/image/getV2?datasetName={}&version={}&ownerTeamId={}".format(name, version, ownerid)
        resp = requests.get(uri)
        if resp.status_code != 200:
            return []
        j = json.loads(resp.content)
        if j["status"]["code"] != 200:
            return []
        return j["data"]["dataItemList"]

    '''
    获取itemLabel: 
    http://thetis.c5-cloudml.xiaomi.srv/image/getItemLabelV2?datasetName=wttest3&version=1&ownerTeamId=3797&itemhash=02abd6f300a0dbf1d0275d5d20684358db857638
    response:
    {
        "status":{
            "code":200,
            "message": success
        },
        "data":{
            "label":["car", "people"],
            "fdsUrl":"cnbj1.fds.api.xiaomi.com/thetis/3bb6c1d91b57804d0cdf2b8533799816"
        }
    }
    '''
    def get_item_label(self, ownerid, name, version, hash):
        ownerid = self._get_digit_id(ownerid)
        uri = "http://" + self.endpoint + "/image/getItemLabelV2?datasetName={}&version={}&ownerTeamId={}&itemhash={}".format(name, version, ownerid, hash)
        resp = requests.get(uri)
        if resp.status_code != 200:
            return None
        j = json.loads(resp.content)
        if j["status"]["code"] != 200:
            return None
        return j["data"]

    '''
    获取 specific file info
    http://dushulin.thetis.c5-cloudml-staging.xiaomi.srv/image/get?datasetName=wttest3&version=1&ownerTeamId=3797&filterpath=xxx
    '''
    def get_item_file(self, ownerid, name, version, path):
        ownerid = self._get_digit_id(ownerid)
        uri = "http://" + self.endpoint + "image/get?datasetName={}&version={}&ownerTeamId={}&filterpath={}".format(name, version, ownerid, path)
        resp = requests.get(uri)
        if resp.status_code != 200:
            return None
        j = json.loads(resp.content)
        if j["status"]["code"] != 200:
            return None
        return j["data"]


# stub for dataset from AD-DP sdk
class ADDPStub(StubBase):
    pass


#stub for Thetis dataset from CloudML sdk
class ThetisCloudmlStub(StubBase):
    pass


def gen_visit_stub_from_adrn(adrn) -> StubBase:
    srv_name, project_name, _, _, _, _ = parse_adrn(adrn)
    if srv_name in ["data-set", "dataset-anno", "data-item", "data-file"]:
        return ThetisHttpStub(project_name)
    else:
        raise Exception("srv_name : {}  is not support in cloudml-pytorch-assistant currently! ".format(srv_name))