import asyncio

import src.core.python.utils.watchfish
from core.python.utils import VideoTypes
from src.core.python.player.play_videos import play

timer = src.core.python.utils.watchfish.Timer()
async def is_time_to_start():
    if timer.is_time_to_start():
        play(VideoTypes.UNKNOWN)
    await asyncio.sleep(30)

asyncio.run(is_time_to_start())
