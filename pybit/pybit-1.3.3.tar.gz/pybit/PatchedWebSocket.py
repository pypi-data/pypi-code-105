# from @zlerba (mx) via @VierX (Markus) on Telegram


import json
from pybit import WebSocket as PybitWebSocket

from time import sleep


class PatchedWebSocket(PybitWebSocket):
    def init(self, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = callback

    def _on_message(self, message):
        msg_json = json.loads(message)
        if 'success' in msg_json:
            if msg_json['success']:
                if 'request' in msg_json:
                    if msg_json['request']['op'] == 'auth':
                        self.logger.debug('Authorization successful.')
                        self.auth = True
                    if msg_json['request']['op'] == 'subscribe':
                        sub = msg_json['request']['args']
                        self.logger.debug(f'Subscription to {sub} successful.')
            else:
                response = msg_json['ret_msg']
                if 'unknown topic' in response:
                    self.logger.error('Couldn\'t subscribe to topic.'
                                      f' Error: {response}.')
                elif msg_json['request']['op'] == 'auth':
                    self.logger.debug('Authorization failed. Please check your '
                                      'API keys and restart.')
        elif 'topic' in msg_json:
            self.callback(msg_json)


def callback_function(message):
    print("callback_function")
    print(message)


subs = ["orderBookL2_25.BTCUSD"]
ws = PatchedWebSocket(endpoint="wss://stream-testnet.bybit.com/realtime", subscriptions=subs)

while True:
    x = ws.fetch(subs[0])
    print(x)
    sleep(1)