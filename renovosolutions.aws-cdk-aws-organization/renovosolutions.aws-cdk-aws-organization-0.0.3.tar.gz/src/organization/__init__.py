'''
# cdk-library-aws-organization

This CDK library is a WIP and not ready for production use.

## Key challenges with Organizations

* Accounts aren't like AWS resources and the [removal process isn't a simple delete](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_remove.html). Therefore the constructs contained in this library do **not** have the goal to delete accounts.
* CloudFormation doesn't support Organizations directly so the constructs in this library use CloudFormation custom resources that utilize Python and [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/organizations.html)

## Testing the custom provider code with SAM CLI

* Create a test project that utilizes this library
* Create a test stack
* Synthesize the test stack with `cdk synth --no-staging > template.yml`
* Get the function name from the template
* Run `sam local start-lambda -t template.yml`
* Run the `handler_tests` python files with `pytest` like follows:

```
LAMBDA_FUNCTION_NAME='<name you noted earlier>' pytest ./handler_tests/<handler>/test.py -rA --capture=sys
```
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
        allow_merge_on_move: typing.Optional[builtins.bool] = None,
        allow_recreate_on_update: typing.Optional[builtins.bool] = None,
        import_on_duplicate: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param name: The name of the OU.
        :param parent_id: The parent OU id.
        :param provider: The provider to use for the custom resource that will create the OU. You can create a provider with the OrganizationOuProvider class
        :param allow_merge_on_move: Whether or not to merge an OU with a duplicate when an OU is moved between parent OUs. If this is false and the OU already exists an error will be thrown. If this is true and the OU already exists the accounts in the OU will be moved to the existing OU and the duplicate, now empty, OU will be deleted. Default: false
        :param allow_recreate_on_update: Whether or not a missing OU should be recreated during an update. If this is false and the OU does not exist an error will be thrown when you try to update it.
        :param import_on_duplicate: Whether or not to import an existing OU if the new OU is a duplicate. If this is false and the OU already exists an error will be thrown. Default: false
        '''
        props = OrganizationOUProps(
            name=name,
            parent_id=parent_id,
            provider=provider,
            allow_merge_on_move=allow_merge_on_move,
            allow_recreate_on_update=allow_recreate_on_update,
            import_on_duplicate=import_on_duplicate,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-aws-organization.OrganizationOUProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "parent_id": "parentId",
        "provider": "provider",
        "allow_merge_on_move": "allowMergeOnMove",
        "allow_recreate_on_update": "allowRecreateOnUpdate",
        "import_on_duplicate": "importOnDuplicate",
    },
)
class OrganizationOUProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        parent_id: builtins.str,
        provider: aws_cdk.custom_resources.Provider,
        allow_merge_on_move: typing.Optional[builtins.bool] = None,
        allow_recreate_on_update: typing.Optional[builtins.bool] = None,
        import_on_duplicate: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param name: The name of the OU.
        :param parent_id: The parent OU id.
        :param provider: The provider to use for the custom resource that will create the OU. You can create a provider with the OrganizationOuProvider class
        :param allow_merge_on_move: Whether or not to merge an OU with a duplicate when an OU is moved between parent OUs. If this is false and the OU already exists an error will be thrown. If this is true and the OU already exists the accounts in the OU will be moved to the existing OU and the duplicate, now empty, OU will be deleted. Default: false
        :param allow_recreate_on_update: Whether or not a missing OU should be recreated during an update. If this is false and the OU does not exist an error will be thrown when you try to update it.
        :param import_on_duplicate: Whether or not to import an existing OU if the new OU is a duplicate. If this is false and the OU already exists an error will be thrown. Default: false
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "parent_id": parent_id,
            "provider": provider,
        }
        if allow_merge_on_move is not None:
            self._values["allow_merge_on_move"] = allow_merge_on_move
        if allow_recreate_on_update is not None:
            self._values["allow_recreate_on_update"] = allow_recreate_on_update
        if import_on_duplicate is not None:
            self._values["import_on_duplicate"] = import_on_duplicate

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

    @builtins.property
    def allow_merge_on_move(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to merge an OU with a duplicate when an OU is moved between parent OUs.

        If this is false and the OU already exists an error will be thrown.
        If this is true and the OU already exists the accounts in the OU will be moved to the existing OU
        and the duplicate, now empty, OU will be deleted.

        :default: false
        '''
        result = self._values.get("allow_merge_on_move")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_recreate_on_update(self) -> typing.Optional[builtins.bool]:
        '''Whether or not a missing OU should be recreated during an update.

        If this is false and the OU does not exist an error will be thrown when you try to update it.
        '''
        result = self._values.get("allow_recreate_on_update")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def import_on_duplicate(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to import an existing OU if the new OU is a duplicate.

        If this is false and the OU already exists an error will be thrown.

        :default: false
        '''
        result = self._values.get("import_on_duplicate")
        return typing.cast(typing.Optional[builtins.bool], result)

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
