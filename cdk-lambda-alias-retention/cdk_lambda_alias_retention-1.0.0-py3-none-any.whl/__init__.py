'''
# replace this
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_lambda
import aws_cdk.core


class LambdaAliasRetention(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-lambda-alias-retention.LambdaAliasRetention",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        fn: aws_cdk.aws_lambda.Function,
        lambda_alias: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param fn: 
        :param lambda_alias: 
        '''
        props = LambdaAliasRetentionProps(fn=fn, lambda_alias=lambda_alias)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-lambda-alias-retention.LambdaAliasRetentionProps",
    jsii_struct_bases=[],
    name_mapping={"fn": "fn", "lambda_alias": "lambdaAlias"},
)
class LambdaAliasRetentionProps:
    def __init__(
        self,
        *,
        fn: aws_cdk.aws_lambda.Function,
        lambda_alias: builtins.str,
    ) -> None:
        '''
        :param fn: 
        :param lambda_alias: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "fn": fn,
            "lambda_alias": lambda_alias,
        }

    @builtins.property
    def fn(self) -> aws_cdk.aws_lambda.Function:
        result = self._values.get("fn")
        assert result is not None, "Required property 'fn' is missing"
        return typing.cast(aws_cdk.aws_lambda.Function, result)

    @builtins.property
    def lambda_alias(self) -> builtins.str:
        result = self._values.get("lambda_alias")
        assert result is not None, "Required property 'lambda_alias' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaAliasRetentionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "LambdaAliasRetention",
    "LambdaAliasRetentionProps",
]

publication.publish()
