"""
only fetches websocket messages within the function; cannot run other code
fetches messages with an async while loop
"""

import asyncio
import websockets
import json


async def hello():
    uri = "wss://stream-testnet.bybit.com/realtime"
    async with websockets.connect(uri) as websocket:
        message = json.dumps({
                    'op': 'subscribe',
                    'args': ["orderBookL2_25.BTCUSD"]
                })

        await websocket.send(message)
        print(f">>> {message}")

        while True:
            response = await websocket.recv()
            print(f"<<< {response}")

if __name__ == "__main__":
    asyncio.run(hello())
    #from time import sleep
    #while True:
    #    print(sleep(0.1))
    #    print("here")
