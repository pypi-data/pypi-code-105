import logging
exokb=bool
exokv=hasattr
exoka=set
exokX=True
exokm=False
exokF=isinstance
exokA=dict
exokl=getattr
exokt=None
exokT=str
exokD=Exception
exokN=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
import dill
from localstack.utils.common import ObjectIdHashComparator
API_STATES_DIR="api_states"
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[exokb,Set]:
 if exokv(obj,"__dict__"):
  visited=visited or exoka()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return exokX,visited
  visited.add(wrapper)
 return exokm,visited
def get_object_dict(obj):
 if exokF(obj,exokA):
  return obj
 obj_dict=exokl(obj,"__dict__",exokt)
 return obj_dict
def is_composite_type(obj):
 return exokF(obj,(exokA,OrderedDict))or exokv(obj,"__dict__")
def api_states_traverse(api_states_path:exokT,side_effect:Callable[...,exokt],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except exokD as e:
    LOG.warning(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with exokN(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except exokD as e:
   LOG.debug("Unable to read pickled persistence file %s: %s"%(state_file,e))
def persist_object(obj,state_file):
 with exokN(state_file,"wb")as f:
  result=f.write(dill.dumps(obj))
  return result
# Created by pyminifier (https://github.com/liftoff/pyminifier)
