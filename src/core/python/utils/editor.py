from json import load, dump

from src.directories import CONFIGS_PATH


class ConfigEditor:
    def __init__(self):
        self.config = {}
        self.config_path = CONFIGS_PATH / "settings.json"

    def _load(self):
        with open(self.config_path, 'r', encoding='UTF-8') as f:
            self.config = load(f)

    def _edit(self, key, value):
        self.config[key] = value

    def _save(self):
        with open(self.config_path, 'w', encoding='UTF-8') as f:
            dump(self.config, f, ensure_ascii=False, indent=2)

    def get(self, key):
        return self.config[key]

    def setconfig(self, key, value):
        self._load()
        self._edit(key, value)
        self._save()