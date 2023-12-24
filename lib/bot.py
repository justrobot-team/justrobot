import asyncio

from .config.config import Config
from .core.bot import Bot


# noinspection PyMethodMayBeStatic
class JustRobot:

    def __init__(self):
        self.Config = Config()
        self.Bot = Bot()
        self.cfg = {}

    def load(self):
        _config_bot, _config_adapter, _config_translator, _config_plugin = asyncio.run(self.Config.read_config())

        _config_adapter, _config_translator, _config_plugin = self._translate_cfg(
            cfg=[_config_adapter, _config_translator, _config_plugin]
        )

        self.cfg = {
            'bot': _config_bot,
            'adapter': _config_adapter,
            'translator': _config_translator,
            'plugin': _config_plugin
        }
        self.Bot.load(self.cfg)

    def _translate_cfg(self, cfg):
        _return = []
        for _cfg in cfg:
            _return.append({_i['name']: _i.pop('name') for _i in _cfg})
        return _return

    def run(self):
        self.Bot.run()
