from pathlib import Path

from PySide6.QtCore import QObject, Slot

# Define paths
# SRC_PATH = Path(__file__).parents[1]
SRC_PATH = Path(__file__).parents[0]
ROOT_PATH = SRC_PATH.parent

QML_PATH = SRC_PATH / "ui" / "qml"

DRIVER_PATH = ROOT_PATH / "drivers"
ASSETS_PATH = ROOT_PATH / "assets"
CONFIGS_PATH = ROOT_PATH / "configs"
# PLUGINS_PATH = ROOT_PATH / "plugins"
LOGS_PATH = ROOT_PATH / "logs"

PATHS = [
    SRC_PATH,
    ASSETS_PATH,
    QML_PATH,
]


class PathManager(QObject):
    def __init__(self):
        super().__init__()

    @Slot(str, result=str)
    def root(self, path_name: str) -> str:
        return ROOT_PATH.joinpath(path_name).resolve().as_uri()

    @Slot(str, result=str)
    def assets(self, path_name: str) -> str:
        return ASSETS_PATH.joinpath(path_name).resolve().as_uri()

    @Slot(str, result=str)
    def images(self, path_name: str) -> str:
        return ASSETS_PATH.joinpath("images", path_name).resolve().as_uri()


if __name__ == "__main__":
    for path in PATHS:
        print(path)
