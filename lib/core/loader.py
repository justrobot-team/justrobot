import asyncio

from ..adapters.loader import Adapter
from ..plugins.loader import Plugin
from ..translators.loader import Translator


class Loader:

    def __init__(self, cfg) -> None:
        self._adapter = Adapter(cfg['adapter'])
        self._translator = Translator(cfg['translator'])
        self._plugin = Plugin(cfg["plugin"])
        self.bot = None
        self.cfg = cfg
        self.adapters = {}
        self.translators = {}
        self.plugins = {}

    async def load(self, bot):
        self.bot = bot
        self.adapters = await self._adapter.load(bot)
        self.translators = await self._translator.load(bot)
        self.plugins = await self._plugin.load(bot)

        [setattr(_translators, 'use_tree', False) for _, _translators in self.translators.items()]
        [setattr(_plugin, 'use_tree', False) for _, _plugin in self.plugins.items()]

        self.bot.adapter_name_list = [_name for _name in self.adapters]
        self.bot.translator_name_list = [_name for _name in self.translators]
        self.bot.plugin_name_list = [_name for _name in self.plugins]

        return self.translators, self.plugins

    async def run(self):
        if not self.adapters:
            await self.bot.log.info({
                'zh': '[Bot] 未检测到可用适配器',
                'en': '[Bot] No adapter detected'
            })
            input('')
        for _, _adapter in self.adapters.items():
            await _adapter.load(self.bot, self.cfg['adapter'])

        self.bot.loop = (asyncio.create_task(_Adapter.run()) for _, _Adapter in self.adapters.items())

        await asyncio.gather(
            *self.bot.loop,
            return_exceptions=True
        )
