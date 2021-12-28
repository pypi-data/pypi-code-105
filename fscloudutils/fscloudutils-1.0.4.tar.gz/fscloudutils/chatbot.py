import sys
import os

# root directory of the project
ROOT_DIR = os.path.abspath("../../")
# import other modules of the project
sys.path.append(ROOT_DIR)
import settings
import requests
import json


class SlackMessenger:
    def __init__(self, block_name, slack_channel=None):
        self.block_name = block_name

        self.parse_ssm_file()
        self.slack_token = settings.slack_token
        if self.environment in ["INTGR", "STAGE"]:
            self.slack_channel = settings.slack_channel_private
        else:
            self.slack_channel = settings.slack_channel_public
        self.slack_icon_emoji = ':beer:'
        self.slack_user_name = 'Beer'

    def parse_ssm_file(self):
        try:
            with open('/tmp/ssm.txt', 'r') as f:
                for line in f.readlines():
                    if "APP_METHOD" in line:
                        self.app_method = line.split("=")[1].replace("\n", "")
                    elif "INSTANCE_TYPE" in line:
                        self.instance_type = line.split("=")[1].replace("\n", "")
                    elif "DEFAULT_BUCKET" in line:
                        self.environment = line.split("-")[1].upper()
        except FileNotFoundError as err:
            self.app_method = "UNKNOWN-METHOD"
            self.instance_type = "UNKNOWN-TYPE"
            self.environment = "STAGE"

        if self.app_method == "analysis":
            self.log_url = settings.analysis_error_log_url.format(self.environment, self.instance_type, self.app_method, self.block_name)
        else:
            self.log_url = settings.calibration_error_log_url.format(self.environment, self.instance_type, self.app_method, self.block_name)

    def to_slack(self, message, file_name=None, file_txt=None):
        if file_name is None:
            self.post_message_to_slack(message)
        else:
            self.post_file_to_slack(message, file_name, file_txt)
        pass

    def post_message_to_slack(self, message, blocks=None):
        return requests.post('https://slack.com/api/chat.postMessage', {
            'token': self.slack_token,
            'channel': self.slack_channel,
            'text': self.generate_message(message),
            'icon_emoji': self.slack_icon_emoji,
            'username': self.slack_user_name,
            'blocks': json.dumps(blocks) if blocks else None
        }).json()

    def post_file_to_slack(self, text, file_name, file_bytes, file_type=None, title=None):
        return requests.post(
            'https://slack.com/api/files.upload',
            {
                'token': self.slack_token,
                'filename': file_name,
                'channels': self.slack_channel,
                'filetype': file_type,
                'initial_comment': text,
                'title': title
            },
            files={'file': file_bytes}).json()

    def generate_message(self, message):
        return "Hey guys, sorry for giving you the bad news but there is a problem with {}.\n" \
               "Traceback: {}\n" \
               "Link to CloudWatch: {}\n**********************************\n".format(self.block_name, message, self.log_url)


def to_sns(message):
    pass


def post_message_to_slack(plot_name, message, cw_link):
    slack_m = SlackMessenger()
    slack_m.to_slack("hi")

    # to_sns(message)


if __name__ == '__main__':
    settings.init()
    slack_m = SlackMessenger("TEST1234")

    slack_m.to_slack("Error in STAGE_EXAMPLE123_DEEP\n"
                     "\n"
                     "TRACEBACK TRACEBACK TRACEBACK\n"
                     "\n"
                     "Link to cloudwatch"
                     )
    slack_m.parse_ssm_file()
