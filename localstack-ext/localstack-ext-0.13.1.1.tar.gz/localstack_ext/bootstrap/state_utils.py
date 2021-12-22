import logging
xKnHt=bool
xKnHB=hasattr
xKnHY=set
xKnHS=True
xKnHd=False
xKnHo=isinstance
xKnHU=dict
xKnHp=getattr
xKnHT=None
xKnHi=str
xKnHA=Exception
xKnHw=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
import dill
from localstack.utils.common import ObjectIdHashComparator
API_STATES_DIR="api_states"
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[xKnHt,Set]:
 if xKnHB(obj,"__dict__"):
  visited=visited or xKnHY()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return xKnHS,visited
  visited.add(wrapper)
 return xKnHd,visited
def get_object_dict(obj):
 if xKnHo(obj,xKnHU):
  return obj
 obj_dict=xKnHp(obj,"__dict__",xKnHT)
 return obj_dict
def is_composite_type(obj):
 return xKnHo(obj,(xKnHU,OrderedDict))or xKnHB(obj,"__dict__")
def api_states_traverse(api_states_path:xKnHi,side_effect:Callable[...,xKnHT],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except xKnHA as e:
    LOG.warning(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with xKnHw(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except xKnHA as e:
   LOG.debug("Unable to read pickled persistence file %s: %s"%(state_file,e))
def persist_object(obj,state_file):
 with xKnHw(state_file,"wb")as f:
  result=f.write(dill.dumps(obj))
  return result
# Created by pyminifier (https://github.com/liftoff/pyminifier)
