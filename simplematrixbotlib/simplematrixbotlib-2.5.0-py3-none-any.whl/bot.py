import asyncio
from typing import Optional
import simplematrixbotlib as botlib
from nio import SyncResponse


class Bot:
    """
    A class for the bot library user to interact with.
    
    ...

    Attributes
    ----------
    api : simplematrixbotlib.Api
        An instance of the simplematrixbotlib.Api class.
    
    """
    def __init__(self, creds, config = None):
        """
        Initializes the simplematrixbotlib.Bot class.

        Parameters
        ----------
        creds : simplematrixbotlib.Creds

        """

        self.creds = creds
        self.api = botlib.Api(self.creds)
        if config:
            self.config = config
        else:
            self.config = botlib.Config()
            # allow (only) users from our own homeserver by default
            hs: str = self.api.async_client.user_id[self.api.async_client.user_id.index(":")+1:].replace('.', '\\.')
            self.config.set_allowlist(set(f".*:{hs}"))
        self.listener = botlib.Listener(self)

    async def main(self):

        self.creds.session_read_file()

        await self.api.login()
        
        self.async_client = self.api.async_client


        resp = await self.async_client.sync(timeout=65536,
                                     full_state=False)  #Ignore prior messages

        if isinstance(resp, SyncResponse):
            print(f"Connected to {self.async_client.homeserver} as {self.async_client.user_id} ({self.async_client.device_id})")

        self.creds.session_write_file()

        self.callbacks = botlib.Callbacks(self.async_client, self)
        await self.callbacks.setup_callbacks()

        for action in self.listener._startup_registry:
            for room_id in self.async_client.rooms:
                await action(room_id)

        await self.async_client.sync_forever(timeout=3000, full_state=True)

    def run(self):
        """
        Runs the bot.

        """

        asyncio.get_event_loop().run_until_complete(self.main())
