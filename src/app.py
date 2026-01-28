import sys
from PySide6.QtWidgets import QApplication

from RinUI import RinUIWindow

from loguru import logger

from src.core.central import AppCentral

logger.add("./logs/app.log", rotation="10 MB", retention="10 days", level="DEBUG")

if __name__ == '__main__':
    logger.info("App started.")
    app = QApplication(sys.argv)
    gallery = RinUIWindow("./qml/app.qml")
    instance = AppCentral()
    gallery.engine.rootContext().setContextProperty("AppCentral", instance)
    app.exec()
    logger.info("App ended.")