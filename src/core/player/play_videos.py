from loguru import logger
from src.core.watchfish import Videos, VideoTypes


def play(video_type: VideoTypes) -> None:
    videos = Videos()
    if video_type == VideoTypes.UNKNOWN:
        video_type = videos.get_video_type()
    logger.info(f"Today's video type: {video_type}")
    if video_type == VideoTypes.NEWS:
        logger.info("Playing news video...")
        from src.core.player.news.xw30f import Play
        player = Play()
        player.open_page()

    elif video_type == VideoTypes.DOCUMENTARY:
        logger.info("Playing documentary video...")
        # player = PlayDocumentary()
        # todo: playing documentary
    else:
        logger.warning("Unknown video type. Cannot play video.")
