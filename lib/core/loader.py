import asyncio

from ..adapters.loader import Adapter
from ..plugins.loader import Plugin
from ..translators.loader import Translator


class Loader:
    """
    中文:
    用于加载插件、适配器、翻译器。

    属性:
        bot: Bot对象
        adapters: 适配器对象
        translators: 翻译器对象
        plugins: 插件对象
        cfg: 配置文件

    私有属性:
        _adapter: 适配器加载器
        _translator: 翻译器加载器
        _plugin: 插件加载器

    方法:
        load: 加载适配器、翻译器、插件
        run: 运行适配器

    English:
    Used to load plugins, adapters, translators.

    Attributes:
        bot: Bot object
        adapters: Adapter object
        translators: Translator object
        plugins: Plugin object
        cfg: Configuration file

    Private attributes:
        _adapter: Adapter loader
        _translator: Translator loader
        _plugin: Plugin loader

    Methods:
        load: Load adapters, translators, plugins
        run: Run adapter
    """

    def __init__(
            self,
            cfg: dict
    ) -> None:
        """
        中文:
        初始化加载器。
        :param cfg: 配置文件。
        :return: None.

        English:
        Initialize the loader.
        :param cfg: Configuration file.
        :return: None.
        """
        self._adapter = Adapter(cfg['adapter'])
        self._translator = Translator(cfg['translator'])
        self._plugin = Plugin(cfg["plugin"])
        self.bot = None
        self.cfg = cfg
        self.adapters: dict = { }
        self.translators: dict = { }
        self.plugins: dict = { }

    async def load(
            self,
            bot: object
    ) -> tuple:
        """
        中文:
        加载适配器、翻译器、插件。
        :param bot: 机器人上下文对象。
        :return: Tuple: 翻译器、插件。

        English:
        Load adapters, translators, plugins.
        :param bot: Bot context object.
        :return: Tuple: Translator, Plugin.
        """
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

    async def run(
            self
    ) -> None:
        """
        中文:
        启动适配器。
        :return: None.

        English:
        Start the adapter.
        :return: None.
        """
        if not self.adapters:
            await self.bot.log.info(
                {
                    'zh': '[Bot] 未检测到可用适配器',
                    'en': '[Bot] No adapter detected'
                }
            )
            input('')
        for _, _adapter in self.adapters.items():
            await _adapter.load(self.bot, self.cfg['adapter'])

        self.bot.loop = (asyncio.create_task(_Adapter.run()) for _, _Adapter in self.adapters.items())

        self.bot.main_loop = asyncio.gather(
            *self.bot.loop,
            return_exceptions=True
        )
        await self.bot.main_loop
