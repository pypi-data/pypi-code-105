'''
[![NPM version](https://badge.fury.io/js/cdk-lambda-alias-retention.svg)](https://badge.fury.io/js/cdk-lambda-alias-retention)
[![PyPI version](https://badge.fury.io/py/cdk-lambda-alias-retention.svg)](https://badge.fury.io/py/cdk-lambda-alias-retention)
[![Release](https://github.com/kimisme9386/cdk-lambda-alias-retention/actions/workflows/release.yml/badge.svg)](https://github.com/kimisme9386/cdk-lambda-alias-retention/actions/workflows/release.yml)

# cdk-lambda-alias-retention

Create lambda alias and retain it forever.

## What's the problem?

When using AWS CDK to create lambda with version and alias, it will retain the latest alias only. See the sample code as blow:

```python
# Example automatically generated from non-compiling source. May contain errors.
const fn = new lambda.DockerImageFunction(stackTest, 'TestLambda', {
    code: lambda.DockerImageCode.fromImageAsset(
    path.join(__dirname, '../lambda'),
    ),
    currentVersionOptions: {
    removalPolicy: RemovalPolicy.RETAIN,
    },
});

fn.currentVersion.addAlias('v1.0.0');
```

In general, the lambda code will be iterated continuously and the alias will be changed probably ever time, such as `v1.0.1`, `v1.0.2`, `v1.0.3` etc...

AWS CDK don't support to retain old alias now and it support to retain old version only.

## Usage

```python
# Example automatically generated from non-compiling source. May contain errors.
new LambdaAliasRetention(stackTest, 'TestLambdaAliasRetention', {
    fn,
    lambdaAlias: 'v1',
});
```

Complete sample code is in [src/integ.default.ts](src/integ.default.ts)

> It can use context or environemnt variable for lambdaAlias.
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
import constructs


class LambdaAliasRetention(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-lambda-alias-retention.LambdaAliasRetention",
):
    def __init__(
        self,
        scope: constructs.Construct,
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
