import asyncio

import core.timer
from core.parser import VideoTypes
from core.player import play

timer = core.timer.Timer()
async def is_time_to_start():
    if timer.is_time_to_start():
        play(VideoTypes.UNKNOWN)
    await asyncio.sleep(30)

asyncio.run(is_time_to_start())
