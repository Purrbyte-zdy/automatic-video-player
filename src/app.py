import sys
from json import load, dump
from PySide6.QtWidgets import QApplication
from RinUI import RinUIWindow
from loguru import logger

from src.core.python import setup_system_tray, ROOT_PATH
from src.core.python.directories import CONFIG_PATH, LOGS_PATH, DRIVER_PATH
from src.ui.python.central import AppCentral

config_file = CONFIG_PATH / "settings.json"
with open(config_file, 'r+', encoding='UTF-8') as f:
    config = load(f)
    if config["first_launch"]:
        LOGS_PATH.mkdir(exist_ok=True)
        DRIVER_PATH.mkdir(exist_ok=True)
        config["first_launch"] = False
        f.seek(0)
        dump(config, f, ensure_ascii=False, indent=4)

# noinspection SpellCheckingInspection
logger.add(sink=ROOT_PATH / "logs/AVP_{{time:YYYYMMDD-HHmmss}}_{version}.log".format(version=config["app_version"]),
           rotation="10 MB",
           retention="10 days",
           level="DEBUG")

if __name__ == '__main__':
    logger.info("App started.")
    app = QApplication(sys.argv)
    gallery = RinUIWindow("./ui/qml/app.qml")
    instance = AppCentral()
    gallery.engine.rootContext().setContextProperty("AppCentral", instance)
    # setup_system_tray(app, gallery)
    app.exec()
    logger.info("App ended.")