from localstack.utils.aws import aws_models
hDUKf=super
hDUKa=None
hDUKk=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  hDUKf(LambdaLayer,self).__init__(arn)
  self.cwd=hDUKa
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.hDUKk.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,hDUKk,env=hDUKa):
  hDUKf(RDSDatabase,self).__init__(hDUKk,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,hDUKk,env=hDUKa):
  hDUKf(RDSCluster,self).__init__(hDUKk,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,hDUKk,env=hDUKa):
  hDUKf(AppSyncAPI,self).__init__(hDUKk,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,hDUKk,env=hDUKa):
  hDUKf(AmplifyApp,self).__init__(hDUKk,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,hDUKk,env=hDUKa):
  hDUKf(ElastiCacheCluster,self).__init__(hDUKk,env=env)
class TransferServer(BaseComponent):
 def __init__(self,hDUKk,env=hDUKa):
  hDUKf(TransferServer,self).__init__(hDUKk,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,hDUKk,env=hDUKa):
  hDUKf(CloudFrontDistribution,self).__init__(hDUKk,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,hDUKk,env=hDUKa):
  hDUKf(CodeCommitRepository,self).__init__(hDUKk,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
