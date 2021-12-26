'''
# aws-cdk-billing-alarm

[![Build status](https://github.com/alvyn279/aws-cdk-billing-alarm/workflows/build/badge.svg)](https://github.com/alvyn279/aws-cdk-billing-alarm/actions/)
[![NPM version](https://badge.fury.io/js/aws-cdk-billing-alarm.svg)](https://www.npmjs.com/package/aws-cdk-billing-alarm)
[![PyPI version](https://badge.fury.io/py/aws-cdk-billing-alarm.svg)](https://pypi.org/project/aws-cdk-billing-alarm/)
[![Mentioned in Awesome CDK](https://awesome.re/mentioned-badge.svg)](https://github.com/kolomied/awesome-cdk)

A CDK construct that sets up email notification for when you exceed a given AWS estimated charges amount.

Create this construct in any stack you find appropriate **with only a few lines**. This construct is an implementation of the manual
setup described on [AWS Estimated Charges Monitoring](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/gs_monitor_estimated_charges_with_cloudwatch.html).

## Get Started

### Pre-Requisites

> **IMPORTANT!** Only complete ***Step 1: Enable Billing Alerts*** of the following documentation link. This construct will take
> care of creating the rest of the resources for you.

You must first enable billing alerts from the AWS Console as per [documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/gs_monitor_estimated_charges_with_cloudwatch.html#gs_turning_on_billing_metrics).

Billing alerts will allow your AWS account to start collecting billing metrics (`EstimatedCharges`) on a periodic 6-hour basis.

### Installation

#### [Node documentation](https://www.npmjs.com/package/aws-cdk-billing-alarm)

```shell
npm install --save aws-cdk-billing-alarm
```

#### [Python documentation](https://pypi.org/project/aws-cdk-billing-alarm/)

```shell
pip install aws-cdk-billing-alarm
```

### Usage

```python
# Example automatically generated from non-compiling source. May contain errors.
import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { BillingAlarm } from 'aws-cdk-billing-alarm';

class CdkStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    // Create an alarm that emails `admin@example.com`
    // if estimated charges exceed 50 USD
    new BillingAlarm(this, 'AWSAccountBillingAlarm', {
      monthlyThreshold: 50,
      emails: ['admin@example.com'],
    });
  }
}
```

### Post-Deployment

Confirm the subscription to the newly created topic for the emails you specified as endpoints in `BillingAlarmProps`.
You can do so by clicking on the `SubscribeURL` of the JSON email you received.

> **Note**: If you did not receive the email, you can fire a **Request confirmation** for the subscription from the AWS SNS Console.

## Limitations

* [USD currency](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/monitor_estimated_charges_with_cloudwatch.html#creating_billing_alarm_with_wizard)
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

import constructs


class BillingAlarm(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-billing-alarm.BillingAlarm",
):
    '''A CDK construct that sets up email notification for when you exceed a given AWS estimated charges amount.

    Note: The email addresses used as SNS Topic endpoint must be manually confirmed
    once the stack is deployed.
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        emails: typing.Sequence[builtins.str],
        monthly_threshold: jsii.Number,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param emails: The emails to which the alarm-triggered notification will be sent.
        :param monthly_threshold: Monetary amount threshold in USD that represents the maximum exclusive limit before which the alarm is triggered and the notification sent.
        '''
        props = BillingAlarmProps(emails=emails, monthly_threshold=monthly_threshold)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="aws-cdk-billing-alarm.BillingAlarmProps",
    jsii_struct_bases=[],
    name_mapping={"emails": "emails", "monthly_threshold": "monthlyThreshold"},
)
class BillingAlarmProps:
    def __init__(
        self,
        *,
        emails: typing.Sequence[builtins.str],
        monthly_threshold: jsii.Number,
    ) -> None:
        '''Properties for a BillingAlarm.

        :param emails: The emails to which the alarm-triggered notification will be sent.
        :param monthly_threshold: Monetary amount threshold in USD that represents the maximum exclusive limit before which the alarm is triggered and the notification sent.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "emails": emails,
            "monthly_threshold": monthly_threshold,
        }

    @builtins.property
    def emails(self) -> typing.List[builtins.str]:
        '''The emails to which the alarm-triggered notification will be sent.'''
        result = self._values.get("emails")
        assert result is not None, "Required property 'emails' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def monthly_threshold(self) -> jsii.Number:
        '''Monetary amount threshold in USD that represents the maximum exclusive limit before which the alarm is triggered and the notification sent.'''
        result = self._values.get("monthly_threshold")
        assert result is not None, "Required property 'monthly_threshold' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BillingAlarmProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BillingAlarm",
    "BillingAlarmProps",
]

publication.publish()
