import json
import os
from datetime import datetime


# 定义一个类用于导入配置
# Define class: load configs
# noinspection PyMethodMayBeStatic
class Config:
    """
    中文:
    初始化配置文件

    私有属性:
        _config_bot_path: Bot 配置文件地址
        _config_adapter_path: Adapter 配置文件地址
        _config_translator_path: Translator 配置文件地址
        _config_plugin_path: Plugin 配置文件地址
        _config_bot: Bot 默认配置文件
        _config_adapter: Adapter 默认配置文件
        _config_translator: Translator 默认配置文件
        _config_plugin: Plugin 默认配置文件

    方法:
        read_config: 读取所有配置文件
        update_config: 更新配置文件

    私有方法:
        _read_bot_config: 读取 Bot 配置文件
        _read_config: 读取配置文件
        _initialize_config: 初始化配置文件

    English:
    Initialize the configuration file

    Private attributes:
        _config_bot_path: Bot configuration file address
        _config_adapter_path: Adapter configuration file address
        _config_translator_path: Translator configuration file address
        _config_plugin_path: Plugin configuration file address
        _config_bot: Bot default configuration file
        _config_adapter: Adapter default configuration file
        _config_translator: Translator default configuration file
        _config_plugin: Plugin default configuration file

    Methods:
        read_config: Read all configuration files
        update_config: Update configuration file

    Private methods:
        _read_bot_config: Read Bot configuration file
        _read_config: Read configuration file
        _initialize_config: Initialize configuration file
    """

    # 初始化配置文件相关内容
    # Initialize configuration file related content
    def __init__(self) -> None:
        """
        中文:
        初始化配置文件。
        :return: None.

        English:
        Initialize the configuration file.
        :return: None.
        """
        # 配置文件地址
        # Configuration file path
        self._config_bot_path = './config/bot.json'
        self._config_adapter_path = './config/adapter.json'
        self._config_translator_path = './config/translator.json'
        self._config_plugin_path = './config/plugin.json'
        # 默认配置文件
        # Default configuration file
        self._config_bot = {
            "name": "Paimion",
            "language": "zh",
            "master": {
                "stdin-adapter": [
                    "stdin"
                ]
            },
            "log_level": 4,
            "translator_api": {
                "name": "aliyun",
                "token": {
                    "ak": "",
                    "sk": ""
                }
            }
        }
        self._config_adapter = [
            {
                'name': '',
                'use_tree': False,
                'enable_translator': [
                    '',
                    ''
                ],
                'enable_direct_plugin': [
                    '',
                    ''
                ],
                'enable_plugin': [
                    '',
                    ''
                ]
            }
        ]
        self._config_translator = [
            {
                'name': '',
                'use_tree': False,
                'enable_plugin': [
                    '',
                    ''
                ]
            }
        ]
        self._config_plugin = [
            {
                'name': '',
                'use_tree': False,
                'listen_adapter': [
                    '',
                    ''
                ],
                'listen_translator': [
                    '',
                    ''
                ]
            }
        ]
        # 检查配置文件是否存在
        # Checkout configuration file exists
        for _path in [
            {
                'name': '_config_bot',
                'path': self._config_bot_path
            },
            {
                'name': '_config_adapter',
                'path': self._config_adapter_path
            },
            {
                'name': '_config_translator',
                'path': self._config_translator_path
            },
            {
                'name': '_config_plugin',
                'path': self._config_plugin_path
            }
        ]:

            if not os.path.exists(_path['path']):
                self._initialize_config(path=_path)

    # 读取 Bot 配置文件
    # Read Bot configuration file
    def _read_bot_config(self) -> None:
        """
        中文:
        读取 Bot 配置文件。
        :return: None.

        English:
        Read Bot configuration file.
        :return: None.
        """
        with open(file=self._config_bot_path, mode='r') as _config:

            try:
                for _key, _value in json.load(fp=_config).items():
                    self._config_bot[_key] = _value

            except json.JSONDecodeError:
                _time = datetime.now().strftime('%H:%M:%S:%f')[:-3]
                print(
                    f'[JustRobot]\033[0m[{_time}][ERROR]\033[0m[config] bot.json 读取失败，请重新进行配置'
                )
                print(
                    f'[JustRobot]\033[0m[{_time}][ERROR]\033[0m[config] bot.json Failed to read, please reconfigure'
                )

        with open(file=self._config_bot_path, mode='w') as _config:
            json.dump(obj=self._config_bot, fp=_config, indent=2)

    # 读取其他配置文件
    # Read other configuration files
    def _read_config(
            self,
            _name
    ) -> None:
        """
        中文:
        读取配置文件。
        :param _name: 配置文件名称。
        :return: None.

        English:
        Read configuration file.
        :param _name: Configuration file name.
        :return: None.
        """
        with open(file=getattr(self, f'_config_{_name}_path'), mode='r') as _config:
            try:
                setattr(self, f'_config_{_name}', json.load(fp=_config))
            except json.JSONDecodeError:
                _time = datetime.now().strftime('%H:%M:%S:%f')[:-3]
                print(
                    f'[JustRobot]\033[31m[{_time}]' +
                    f'[ERROR]\033[0m[config] {_name}.json 读取失败，请重新进行配置'
                )
                print(
                    f'[JustRobot]\033[31m[{_time}]' +
                    f'[ERROR]\033[0m[config] {_name}.json Failed to read, please reconfigure'
                )

        with open(file=getattr(self, f'_config_{_name}_path'), mode='w') as _config:
            json.dump(obj=getattr(self, f'_config_{_name}'), fp=_config, indent=2)

    # 读取所有配置文件
    # Read all configuration files
    async def read_config(self) -> tuple:
        """
        中文:
        读取所有配置文件。
        :return: tuple: 所有配置文件。
        """
        self._read_bot_config()
        for _name in ['adapter', 'translator', 'plugin']:
            self._read_config(_name)

        _time = datetime.now().strftime('%H:%M:%S:%f')[:-3]
        print(f'[JustRobot]\033[32m[{_time}][INFO]\033[0m[config] 配置文件载入完成')
        print(f'[JustRobot]\033[32m[{_time}][INFO]\033[0m[config] Configuration load completed')

        return self._config_bot, self._config_adapter, self._config_translator, self._config_plugin

    # 更新配置文件
    # Update configuration file
    async def update_config(
            self,
            bot,
            cfg,
            key,
            value
    ) -> None:
        """
        中文:
        更新配置文件。
        :param bot: Bot 实例。
        :param cfg: 配置文件名称。
        :param key: 配置文件目标键。
        :param value: 配置文件目标键新值。
        :return: None.

        English:
        Update configuration file.
        :param bot: Bot instance.
        :param cfg: Configuration file name.
        :param key: Configuration file target key.
        :param value: Configuration file target key new value.
        :return: None.
        """
        with open(getattr(self, f'_config_{cfg}_path'), 'r') as _f:
            _cfg = json.load(_f)

        setattr(_cfg, key, value)
        with open(getattr(self, f'_config_{cfg}_path'), 'w') as _f:
            json.dump(obj=_cfg, fp=_f, indent=2)

        # noinspection PyProtectedMember
        setattr(bot._config[cfg], key, value)

    # 初始化配置文件
    # Initialize configuration file
    def _initialize_config(
            self,
            path
    ) -> None:
        """
        中文:
        初始化配置文件。
        :param path: 配置文件路径。
        :return: None.
        """
        _config = getattr(self, path['name'])
        _path = path['path']
        with open(_path, 'x') as _f:
            json.dump(obj=_config, fp=_f, indent=2)
