import asyncio

from .core import Core
from .loader import Loader
from .log import Log


# noinspection PyMethodMayBeStatic
class Bot:

    def __init__(self) -> None:
        self._loader = None
        self.log = None
        self.translators = None
        self.plugins = None
        self.bot = None

    def load(self, cfg):
        self._loader = Loader(cfg)
        self.log = Log({
            'level': cfg['bot']['log_level'],
            'lang': cfg['bot']['language']
        })
        asyncio.run(self.log.info(' -------- 欢迎使用 JustRobot  ^_< ---------'))
        self.bot = Core(self.log, cfg['bot'])
        self.bot.loader = self._loader
        self.translators, self.plugins = asyncio.run(self._loader.load(self.bot))
        _adapter_num = len(self.bot.adapter_name_list)
        _translator_num = len(self.bot.translator_name_list)
        _plugin_num = len(self.bot.plugin_name_list)
        asyncio.run(
            self.log.info(f'[Bot] 加载完成，共有{_adapter_num}个适配器，{_translator_num}个转译器，{_plugin_num}个插件')
        )
        self.bot.load({
            'translators': self.translators,
            'plugins': self.plugins
        })

    def run(self):
        asyncio.run(self._loader.run())
