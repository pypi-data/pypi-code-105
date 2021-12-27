# coding: utf-8
import json
import requests
from sentry.plugins.bases.notify import NotificationPlugin

from .forms import DingDingOptionsForm


class DingTalkPlugin(NotificationPlugin):

    DING_TALK = "https://oapi.dingtalk.com/robot/send?access_token="
    VERSION = "1.0.0"

    """
    Sentry plugin to send error counts to DingDing.
    """
    author = 'spxinjie6'
    author_url = 'git@github.com:spxinjie6/sentry-notice.git'
    version = VERSION
    description = '发送dingding 告警'
    resource_links = [
        ('Source', 'https://github.com/cench/sentry-10-dingding'),
        ('Bug Tracker', 'https://github.com/spxinjie6/sentry-notice/issues'),
        ('README', 'https://github.com/spxinjie6/sentry-notice/blob/main/README.md'),
    ]

    slug = 'WbDingDing'  # 页面会显示当前插件
    title = 'WbDingDing'
    conf_key = slug
    conf_title = title
    project_conf_form = DingDingOptionsForm

    def is_configured(self, project):
        """
        Check if plugin is configured.
        """
        return bool(self.get_option('access_token', project))

    def notify_users(self, group, event, *args, **kwargs):
        self.post_process(group, event, *args, **kwargs)

    def post_process(self, group, event, *args, **kwargs):
        """
        Process error.

        :param group: https://github1s.com/getsentry/sentry/blob/HEAD/src/sentry/models/group.py#L385 class Group(Model)
        :param event: https://github1s.com/getsentry/sentry/blob/HEAD/src/sentry/eventstore/models.py#L95
                      https://github1s.com/getsentry/sentry/blob/HEAD/src/sentry/snuba/events.py
        """
        if not self.is_configured(group.project):
            return

        if group.is_ignored():
            return

        access_token = self.get_option('access_token', group.project)
        send_url = f"{self.DING_TALK}{access_token}"
        title = f'【{event.project.slug}】的项目异常'
        # 拼装报警信息
        data = dict(
            msgtype="markdown",
            markdown=dict(
                title=title,
                text=""
            )
        )
        # 根据组进行报警拆分
        teams = [model.name for model in event.project.teams.all()]
        url = f"{group.get_absolute_url()}events/{event.event_id}/"
        if "ops" in teams:
            text = f"""
#### {title} \n\n 
> {event.title or event.message} \n\n
> 集群ID: {event.get_tag("server_name")} \n\n
> class: {event.get_tag("transaction")} \n\n
> 请求链接: {event.get_tag('url')} \n\n
[错误详细]({url})
"""
        else:
            text = f"""
#### {title} \n\n 
> {event.title or event.message} \n\n 
> 设备:{event.get_tag('device')} \n\n
> UID:{event.get_tag('uid')} \n\n
> {event.get_tag('url')} \n\n 
[错误详细]({url})
"""

        data["markdown"]["text"] = text
        requests.post(
            url=send_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data).encode("utf-8")
        )