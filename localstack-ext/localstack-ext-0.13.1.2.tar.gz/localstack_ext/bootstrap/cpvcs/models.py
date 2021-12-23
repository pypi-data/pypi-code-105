from datetime import datetime
EgYkD=str
EgYko=int
EgYkK=super
EgYky=False
EgYkX=isinstance
EgYkh=hash
EgYku=bool
EgYkc=True
EgYkM=list
EgYkv=map
EgYkN=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:EgYkD):
  self.hash_ref:EgYkD=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:EgYkD,rel_path:EgYkD,file_name:EgYkD,size:EgYko,service:EgYkD,region:EgYkD):
  EgYkK(StateFileRef,self).__init__(hash_ref)
  self.rel_path:EgYkD=rel_path
  self.file_name:EgYkD=file_name
  self.size:EgYko=size
  self.service:EgYkD=service
  self.region:EgYkD=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return EgYky
  if not EgYkX(other,StateFileRef):
   return EgYky
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return EgYkh((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other)->EgYku:
  if not other:
   return EgYky
  if not EgYkX(other,StateFileRef):
   return EgYky
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others)->EgYku:
  for other in others:
   if self.congruent(other):
    return EgYkc
  return EgYky
 def metadata(self)->EgYkD:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:EgYkD,state_files:Set[StateFileRef],parent_ptr:EgYkD):
  EgYkK(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:EgYkD=parent_ptr
 def state_files_info(self)->EgYkD:
  return "\n".join(EgYkM(EgYkv(lambda state_file:EgYkD(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:EgYkD,head_ptr:EgYkD,message:EgYkD,timestamp:EgYkD=EgYkD(datetime.now().timestamp()),delta_log_ptr:EgYkD=EgYkN):
  self.tail_ptr:EgYkD=tail_ptr
  self.head_ptr:EgYkD=head_ptr
  self.message:EgYkD=message
  self.timestamp:EgYkD=timestamp
  self.delta_log_ptr:EgYkD=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:EgYkD,to_node:EgYkD)->EgYkD:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:EgYkD,state_files:Set[StateFileRef],parent_ptr:EgYkD,creator:EgYkD,rid:EgYkD,revision_number:EgYko,assoc_commit:Commit=EgYkN):
  EgYkK(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:EgYkD=creator
  self.rid:EgYkD=rid
  self.revision_number:EgYko=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(EgYkv(lambda state_file:EgYkD(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:EgYkD,state_files:Set[StateFileRef],parent_ptr:EgYkD,creator:EgYkD,comment:EgYkD,active_revision_ptr:EgYkD,outgoing_revision_ptrs:Set[EgYkD],incoming_revision_ptr:EgYkD,version_number:EgYko):
  EgYkK(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(EgYkv(lambda stat_file:EgYkD(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
