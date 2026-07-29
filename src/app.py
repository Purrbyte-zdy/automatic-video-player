import os
import sys
from json import load, dump
from PySide6.QtWidgets import QApplication
from RinUI import RinUIWindow
from loguru import logger

# from core.python import setup_system_tray, ROOT_PATH
from directories import ROOT_PATH, CONFIGS_PATH, LOGS_PATH, DRIVER_PATH
from core import AppCentral

config_file = CONFIGS_PATH / "settings.json"
with open(config_file, 'r+', encoding='UTF-8') as f: # Setting First Launch Mode.
    config = load(f)
    if config["first_launch"]:
        LOGS_PATH.mkdir(exist_ok=True)
        DRIVER_PATH.mkdir(exist_ok=True)
        config["first_launch"] = False
        f.seek(0)
        dump(config, f, ensure_ascii=False, indent=4)

# noinspection SpellCheckingInspection
logger.add(sink=ROOT_PATH / "logs/AVP_{{time:MMDDHHmmss}}_{version}.log".format(version=config["app_version"]),
           rotation="4 MB",
           retention="7 days",
           level="DEBUG")

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.insert(0, project_root)

if __name__ == '__main__':
    logger.info("App started.")
    app = QApplication(sys.argv)
    gallery = RinUIWindow("./ui/qml/app.qml")
    instance = AppCentral()
    instance.setup_qml_context(gallery)
    # setup_system_tray(app, gallery)
    app.exec()
    logger.info("App ended.")