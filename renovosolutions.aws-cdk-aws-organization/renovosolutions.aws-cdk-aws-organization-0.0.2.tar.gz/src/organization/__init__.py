'''
# cdk-library-aws-organization

This CDK library is a WIP and not ready for production use.

## Testing the custom provider code with SAM CLI

* Create a test project that utilizes this library
* Create a test stack
* Synthesize the test stack with `cdk synth --no-staging > template.yml`
* Run `sam local invoke <function from stack> -e <event json file>`
* There is some example events provided in the `events` folder, but you will need a real test org to run events against
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

import aws_cdk.aws_iam
import aws_cdk.custom_resources
import constructs


class OrganizationOU(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-aws-organization.OrganizationOU",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        parent_id: builtins.str,
        provider: aws_cdk.custom_resources.Provider,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param name: The name of the OU.
        :param parent_id: The parent OU id.
        :param provider: The provider to use for the custom resource that will create the OU. You can create a provider with the OrganizationOuProvider class
        '''
        props = OrganizationOUProps(name=name, parent_id=parent_id, provider=provider)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-aws-organization.OrganizationOUProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "parent_id": "parentId", "provider": "provider"},
)
class OrganizationOUProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        parent_id: builtins.str,
        provider: aws_cdk.custom_resources.Provider,
    ) -> None:
        '''
        :param name: The name of the OU.
        :param parent_id: The parent OU id.
        :param provider: The provider to use for the custom resource that will create the OU. You can create a provider with the OrganizationOuProvider class
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "parent_id": parent_id,
            "provider": provider,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the OU.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parent_id(self) -> builtins.str:
        '''The parent OU id.'''
        result = self._values.get("parent_id")
        assert result is not None, "Required property 'parent_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider(self) -> aws_cdk.custom_resources.Provider:
        '''The provider to use for the custom resource that will create the OU.

        You can create a provider with the OrganizationOuProvider class
        '''
        result = self._values.get("provider")
        assert result is not None, "Required property 'provider' is missing"
        return typing.cast(aws_cdk.custom_resources.Provider, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationOUProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OrganizationOUProvider(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-aws-organization.OrganizationOUProvider",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param role: The role the custom resource should use for taking actions on OUs if one is not provided one will be created automatically.
        '''
        props = OrganizationOUProviderProps(role=role)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="provider")
    def provider(self) -> aws_cdk.custom_resources.Provider:
        return typing.cast(aws_cdk.custom_resources.Provider, jsii.get(self, "provider"))


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-aws-organization.OrganizationOUProviderProps",
    jsii_struct_bases=[],
    name_mapping={"role": "role"},
)
class OrganizationOUProviderProps:
    def __init__(self, *, role: typing.Optional[aws_cdk.aws_iam.IRole] = None) -> None:
        '''
        :param role: The role the custom resource should use for taking actions on OUs if one is not provided one will be created automatically.
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        '''The role the custom resource should use for taking actions on OUs if one is not provided one will be created automatically.'''
        result = self._values.get("role")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrganizationOUProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "OrganizationOU",
    "OrganizationOUProps",
    "OrganizationOUProvider",
    "OrganizationOUProviderProps",
]

publication.publish()
