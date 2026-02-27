from loguru import logger
from core.python.utils.watchfish import Videos, VideoTypes


def play(video_type: VideoTypes) -> None:
    videos = Videos()
    if video_type == VideoTypes.UNKNOWN:
        video_type = videos.get_video_type()
    logger.info(f"Today's video type: {video_type}")
    if video_type == VideoTypes.NEWS:
        logger.info("Playing news video...")
        from src.core.python.player.news.xw30f import Play
        player = Play()
        finished_status = player.open_page()
        match finished_status:
            case True:
                logger.success("News video playback finished successfully.")
                player.exit_playing()
            case False:
                logger.error("News video playback failed.")

    elif video_type == VideoTypes.DOCUMENTARY:
        logger.info("Playing documentary video...")
        # player = PlayDocumentary()
        # todo: playing documentary
    else:
        logger.warning("Unknown video type. Cannot play video.")
