from localstack.utils.aws import aws_models
wPUiN=super
wPUin=None
wPUiE=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  wPUiN(LambdaLayer,self).__init__(arn)
  self.cwd=wPUin
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.wPUiE.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,wPUiE,env=wPUin):
  wPUiN(RDSDatabase,self).__init__(wPUiE,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,wPUiE,env=wPUin):
  wPUiN(RDSCluster,self).__init__(wPUiE,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,wPUiE,env=wPUin):
  wPUiN(AppSyncAPI,self).__init__(wPUiE,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,wPUiE,env=wPUin):
  wPUiN(AmplifyApp,self).__init__(wPUiE,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,wPUiE,env=wPUin):
  wPUiN(ElastiCacheCluster,self).__init__(wPUiE,env=env)
class TransferServer(BaseComponent):
 def __init__(self,wPUiE,env=wPUin):
  wPUiN(TransferServer,self).__init__(wPUiE,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,wPUiE,env=wPUin):
  wPUiN(CloudFrontDistribution,self).__init__(wPUiE,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,wPUiE,env=wPUin):
  wPUiN(CodeCommitRepository,self).__init__(wPUiE,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
