from datetime import datetime
vWLbY=str
vWLbN=int
vWLbA=super
vWLbn=False
vWLbH=isinstance
vWLbS=hash
vWLby=bool
vWLbO=True
vWLbE=list
vWLbo=map
vWLbV=None
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
class CPVCSObj:
 def __init__(self,hash_ref:vWLbY):
  self.hash_ref:vWLbY=hash_ref
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:vWLbY,rel_path:vWLbY,file_name:vWLbY,size:vWLbN,service:vWLbY,region:vWLbY):
  vWLbA(StateFileRef,self).__init__(hash_ref)
  self.rel_path:vWLbY=rel_path
  self.file_name:vWLbY=file_name
  self.size:vWLbN=size
  self.service:vWLbY=service
  self.region:vWLbY=region
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path)
 def __eq__(self,other):
  if not other:
   return vWLbn
  if not vWLbH(other,StateFileRef):
   return vWLbn
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return vWLbS((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other)->vWLby:
  if not other:
   return vWLbn
  if not vWLbH(other,StateFileRef):
   return vWLbn
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others)->vWLby:
  for other in others:
   if self.congruent(other):
    return vWLbO
  return vWLbn
 def metadata(self)->vWLbY:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:vWLbY,state_files:Set[StateFileRef],parent_ptr:vWLbY):
  vWLbA(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:vWLbY=parent_ptr
 def state_files_info(self)->vWLbY:
  return "\n".join(vWLbE(vWLbo(lambda state_file:vWLbY(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:vWLbY,head_ptr:vWLbY,message:vWLbY,timestamp:vWLbY=vWLbY(datetime.now().timestamp()),delta_log_ptr:vWLbY=vWLbV):
  self.tail_ptr:vWLbY=tail_ptr
  self.head_ptr:vWLbY=head_ptr
  self.message:vWLbY=message
  self.timestamp:vWLbY=timestamp
  self.delta_log_ptr:vWLbY=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:vWLbY,to_node:vWLbY)->vWLbY:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:vWLbY,state_files:Set[StateFileRef],parent_ptr:vWLbY,creator:vWLbY,rid:vWLbY,revision_number:vWLbN,assoc_commit:Commit=vWLbV):
  vWLbA(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:vWLbY=creator
  self.rid:vWLbY=rid
  self.revision_number:vWLbN=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(vWLbo(lambda state_file:vWLbY(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:vWLbY,state_files:Set[StateFileRef],parent_ptr:vWLbY,creator:vWLbY,comment:vWLbY,active_revision_ptr:vWLbY,outgoing_revision_ptrs:Set[vWLbY],incoming_revision_ptr:vWLbY,version_number:vWLbN):
  vWLbA(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(vWLbo(lambda stat_file:vWLbY(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
