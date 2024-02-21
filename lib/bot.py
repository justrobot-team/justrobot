import asyncio

from .config.config import Config
from .core.bot import Bot


# noinspection PyMethodMayBeStatic
class JustRobot:
    """
    中文:
    JustRobot 抽象类, 用于加载配置文件, 并启动机器人

    属性:
        Config: 配置文件类
        Bot: 机器人类
        cfg: 配置文件

    方法:
        load: 加载配置文件、适配器、转译器、插件
        run: 启动机器人

    English:
    JustRobot abstract class, used to load the configuration file and start the robot

    Attributes:
        Config: Configuration file class
        Bot: Robot class
        cfg: Configuration file

    Methods:
        load: Load the configuration, adapter, translator, and plugin
        run: Start the robot
    """

    def __init__(
            self
    ) -> None:
        """
        中文:
        初始化 JustRobot 类
        :return: None.

        English:
        Initialize the JustRobot class
        :return: None.
        """
        self.Config = Config()
        self.Bot = Bot()
        self.cfg = { }

    def load(
            self
    ) -> None:
        """
        中文:
        加载配置文件、适配器、转译器、插件
        :return: None.

        English:
        Load the configuration, adapter, translator, and plugin
        :return: None.
        """
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

    def _translate_cfg(
            self,
            cfg
    ) -> list:
        _return = []
        for _cfg in cfg:
            _return.append({ _i['name']: _i.pop('name') for _i in _cfg })
        return _return

    def run(
            self
    ) -> None:
        """
        中文:
        启动机器人
        :return: None.

        English:
        Start the robot
        :return: None.
        """
        self.Bot.run()
