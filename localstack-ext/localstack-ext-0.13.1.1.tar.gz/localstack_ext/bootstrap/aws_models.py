from localstack.utils.aws import aws_models
rItOa=super
rItOF=None
rItOx=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  rItOa(LambdaLayer,self).__init__(arn)
  self.cwd=rItOF
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.rItOx.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,rItOx,env=rItOF):
  rItOa(RDSDatabase,self).__init__(rItOx,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,rItOx,env=rItOF):
  rItOa(RDSCluster,self).__init__(rItOx,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,rItOx,env=rItOF):
  rItOa(AppSyncAPI,self).__init__(rItOx,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,rItOx,env=rItOF):
  rItOa(AmplifyApp,self).__init__(rItOx,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,rItOx,env=rItOF):
  rItOa(ElastiCacheCluster,self).__init__(rItOx,env=env)
class TransferServer(BaseComponent):
 def __init__(self,rItOx,env=rItOF):
  rItOa(TransferServer,self).__init__(rItOx,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,rItOx,env=rItOF):
  rItOa(CloudFrontDistribution,self).__init__(rItOx,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,rItOx,env=rItOF):
  rItOa(CodeCommitRepository,self).__init__(rItOx,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
