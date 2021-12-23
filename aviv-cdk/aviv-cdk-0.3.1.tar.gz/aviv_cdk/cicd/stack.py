import typing
from constructs import Construct
from aws_cdk import (
    Stack,
    aws_ssm,
    aws_codebuild,
    pipelines
)
from . import (
    sources
)

class CodePipelineStack(Stack):
    __connections: dict={}

    def __init__(
            self, scope: Construct, construct_id: str, *,
            connections: dict=None,
            repository: typing.Union[str, sources.SourceRepositoryAttrs]=None,
            code_build_clone_output: bool=True,
            trigger_on_push: bool=None,
            codepipeline: typing.Union[dict, pipelines.CodePipelineProps]=None,
            **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        if connections:
            self.connections = connections
        self.source = self.sources(repository=repository, code_build_clone_output=code_build_clone_output, trigger_on_push=trigger_on_push)
        self.pipeline = self.codepipeline(source=self.source, **codepipeline)

    def codepipeline(self, source: pipelines.IFileSetProducer, **codepipeline):
        return pipelines.CodePipeline(
            self, "Pipeline",
            code_build_defaults=pipelines.CodeBuildOptions(
                build_environment=aws_codebuild.BuildEnvironment(
                    build_image=aws_codebuild.LinuxBuildImage.AMAZON_LINUX_2_3
                )
            ),
            synth=pipelines.ShellStep(
                "Synth",
                input=source,
                commands=[
                    "npm install -g aws-cdk",
                    "python -m pip install aws-cdk-lib",
                    "cdk synth"
                ]
            ),
            **codepipeline
        )

    def sources(self, repository: typing.Union[str, sources.SourceRepositoryAttrs]=None, code_build_clone_output: bool=None, trigger_on_push: bool=None) -> pipelines.CodePipelineSource:
        if not repository:
            info = sources.git_repository_info()
            repository = f"{info.get('url')}@{info.get('branch')}"
        if isinstance(repository, str):
            repository = sources.git_url_split(repository)

        return pipelines.CodePipelineSource.connection(
            f"{repository['owner']}/{repository['repo']}",
            branch=repository['branch'],
            connection_arn=self.connections[repository['owner']],
            code_build_clone_output=code_build_clone_output,
            trigger_on_push=trigger_on_push
        )

    @property
    def connections(self) -> dict:
        return self.__connections

    @connections.setter
    def connections(self, connections: dict) -> None:
        for cname, connection_arn in connections.items():
            if connection_arn.startswith('aws:ssm:'):
                connection_arn = aws_ssm.StringParameter.value_from_lookup(
                    self, parameter_name=connection_arn.replace('aws:ssm:', '')
                )
            self.__connections[cname] = connection_arn
