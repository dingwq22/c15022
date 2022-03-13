import logging
from utils import loggingtimenow
logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s [%(levelname)s] %(message)s",
)
logging.Formatter.converter = loggingtimenow

import asyncio
import discordbot

import loggingsetup
loggingsetup.setup()

import server

loop=asyncio.get_event_loop()
loop.create_task(server.startserver())
loop.create_task(discordbot.runbot())
loop.run_forever()