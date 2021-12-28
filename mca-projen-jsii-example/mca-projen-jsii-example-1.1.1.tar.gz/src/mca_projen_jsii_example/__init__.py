'''
# MCA Projen JSii Example

[![npm version](https://badge.fury.io/js/mca-projen-jsii-example.svg)](https://badge.fury.io/js/mca-projen-jsii-example)
[![PyPI version](https://badge.fury.io/py/mca-projen-jsii-example.svg)](https://badge.fury.io/py/mca-projen-jsii-example)
[![Maven Central](https://maven-badges.herokuapp.com/maven-central/com.marciocadev/mca-projen-jsii-example/badge.svg)](https://maven-badges.herokuapp.com/maven-central/com.marciocadev/mca-projen-jsii-example)
[![Go Reference](https://pkg.go.dev/badge/github.com/marciocadev/com/mca-projen-jsii-example.svg)](https://pkg.go.dev/github.com/aws/aws-cdk-go/awscdk)
[![release](https://github.com/marciocadev/mca-projen-jsii-example/actions/workflows/release.yml/badge.svg)](https://github.com/marciocadev/mca-projen-jsii-example/actions/workflows/release.yml)

The **MCA Projen JSii Example** it's a test project to learn how deploy at NPM, PyPi and Maven repositories, auto-versioning and runing git actions on commits
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


class Hello(metaclass=jsii.JSIIMeta, jsii_type="mca-projen-jsii-example.Hello"):
    '''My Hello class.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="sayHello")
    def say_hello(self, name: builtins.str) -> builtins.str:
        '''My sayHello function.

        :param name: Someone who calls.

        :return: Greetings
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "sayHello", [name]))


__all__ = [
    "Hello",
]

publication.publish()
