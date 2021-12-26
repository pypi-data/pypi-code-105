import requests
import json
import logging


class Webhook:
    def send_adaptative_card(adaptative_card, webhook):
        content = adaptative_card.get_element()
        data={
            "type":"message",
            "attachments":[
                {
                    "contentType":"application/vnd.microsoft.card.adaptive",
                    "contentUrl": None,
                    "content": content
                }
            ]
        }        
        logging.debug(json.dumps(content))
        response = requests.post(webhook, json=data)
        if response.status_code != 200:
            raise Exception(response.content)