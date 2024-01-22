import asyncio

from .core import Core
from .loader import Loader
from .log import Log


# noinspection PyMethodMayBeStatic
class Bot:
    """
    中文:
    Bot类，用于加载插件和适配器，以及启动Bot

    属性:
        _loader: Loader对象，用于加载插件和适配器
        log: Log对象，用于记录日志
        translators: dict，存储转译器
        plugins: dict，存储插件
        bot: 机器人上下文对象

    方法:
        load: 加载插件和适配器
        run: 启动 Bot

    English:
    Bot class, used to load plugins and adapters, and start the Bot

    Attributes:
        _loader: Loader object, used to load plugins and adapters
        log: Log object, used to record logs
        translators: dict, store translators
        plugins: dict, store plugins
        bot: Bot context object

    Methods:
        load: Load plugins and adapters
        run: Start the Bot
    """

    def __init__(self) -> None:
        """
        中文:
        初始化 Bot 类。
        :return: None.

        English:
        Initialize the Bot class.
        :return: None.
        """
        self._loader = None
        self.log = None
        self.translators = None
        self.plugins = None
        self.bot = None

    def load(
            self,
            cfg
    ) -> None:
        """
        中文:
        加载插件和适配器。
        :param cfg: dict，配置文件
        :return: None.

        English:
        Load plugins and adapters.
        :param cfg: dict, configuration file
        :return: None.
        """
        self._loader = Loader(cfg)
        self.log = Log({
            'level': cfg['bot']['log_level'],
            'lang': cfg['bot']['language']
        })
        asyncio.run(self.log.info({
            'zh': ' -------- 欢迎使用 JustRobot  ^_< ---------',
            'en': ' ----- Welcome to use JustRobot  ^_< ------'
        }))
        self.bot = Core(self.log, cfg['bot'])
        self.bot.loader = self._loader
        self.translators, self.plugins = asyncio.run(self._loader.load(self.bot))
        _adapter_num = len(self.bot.adapter_name_list)
        _translator_num = len(self.bot.translator_name_list)
        _plugin_num = len(self.bot.plugin_name_list)
        asyncio.run(
            self.log.info({
                'zh': f'[Bot] 加载完成，共有{_adapter_num}个适配器，{_translator_num}个转译器，{_plugin_num}个插件',
                'en': f'[Bot] Loaded {_adapter_num} adapters, {_translator_num} translators, {_plugin_num} plugins'
            })
        )
        self.bot.load({
            'translators': self.translators,
            'plugins': self.plugins
        })

    def run(self) -> None:
        """
        中文:
        启动 Bot。
        :return: None.

        English:
        Start the Bot.
        :return: None.
        """
        try:
            asyncio.run(self._loader.run())
        except SystemExit:
            exit()
