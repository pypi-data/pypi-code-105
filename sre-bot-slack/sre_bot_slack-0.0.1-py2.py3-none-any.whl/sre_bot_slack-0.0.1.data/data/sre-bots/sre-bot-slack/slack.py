import requests
import arrow
import json
from pathlib import Path

def post_message_to_slack(channel, text):

    config_file = Path("/etc/sre/slack.conf")
    if not config_file.exists():
        raise Exception(f"Config file missing: {config_file}")

    config = json.loads(config_file.read_text())
    token = config.get('channels', {}).get(channel, None)
    if not token:
        token = config['token']
    return requests.post('https://hooks.slack.com/services/' + token, json={
        "text": text,
        })

def on_message(client, msg, payload=None):
    if '/slack/notify' in msg.topic:

        topic = msg.topic.split("/")
        idx = topic.index('notify') + 1
        channel = None
        if idx < len(topic):
            channel = topic[idx]

        data = json.loads(msg.payload)
        msg = f"{data['module']}: {data['value']}"
        post_message_to_slack(channel, msg)