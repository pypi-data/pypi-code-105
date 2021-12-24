"""
should be able
    however it doesn't run listen_for_message correctly
fetches messages in an async while loop
based on:
"""

import asyncio
import websockets
import json
from time import sleep


async def listen_for_message(websocket):
    print("listen_for_message")

    while True:

        await asyncio.sleep(0)

        try:
            #print('Listening for a message...')
            message = await websocket.recv()

            print(f"< {message}")

        except websockets.ConnectionClosed as cc:
            print('Connection closed')

        except Exception as e:
            #print('Something happened')
            pass


async def connect_to_websocket():

    print('connect to websocket')
    websocket = await websockets.connect("wss://stream-testnet.bybit.com/realtime")

    message = json.dumps({
        'op': 'subscribe',
        'args': ["orderBookL2_25.BTCUSD"]
    })

    await websocket.send(message)

    #hello_message = await websocket.recv()
    #print("< {}".format(hello_message))


async def my_app():

    # this will block until connect_to_dealer() returns
    websocket = await connect_to_websocket()

    print(2)

    # start listen_for_message() in its own task wrapper, so doing it continues in the background
    #asyncio.ensure_future(listen_for_message(websocket))
    await listen_for_message(websocket)

    # you can continue with other code here that can now coexist with listen_for_message()
    while True:
        print(1)
        sleep(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(my_app())
    loop.run_forever()
