#!/bin/python3
# coding=utf-8
# ------------------------------------------------------------------------------
# Created on October 05 12:54 2021
#
# Vertica VCLI (Vertica Command Line Interface)
#       argsparse command line implementation
#
# Usage:
#   va login
#   va login --profile profile2
#
# (c) Copyright 2021 Micro Focus or one of its affiliates.
# ------------------------------------------------------------------------------
from __future__ import annotations
from abc import ABC, abstractmethod


class SubCommandImplementation(ABC):
    @abstractmethod
    def operation_cmd(self, args) -> None:
        pass

    @abstractmethod
    def operation_define(self, subparsers) -> None:
        pass


class SubCommand:
    def __init__(self, implementation: SubCommandImplementation) -> None:
        self.implementation = implementation

    def arg_operation(self, args) -> None:
        self.implementation.operation_cmd(args)

    def arg_define(self, subparsers) -> None:
        self.implementation.operation_define(subparsers)
