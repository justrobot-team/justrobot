import json
import os
from datetime import datetime


# noinspection PyMethodMayBeStatic
class Config:

    def __init__(self):
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
                "adapter_stdin": [
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
            {'name': '',
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

    def _read_bot_config(self):

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

    def _read_config(self, _name):
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

    async def read_config(self):

        self._read_bot_config()
        for _name in ['adapter', 'translator', 'plugin']:
            self._read_config(_name)

        _time = datetime.now().strftime('%H:%M:%S:%f')[:-3]
        print(f'[JustRobot]\033[32m[{_time}][INFO]\033[0m[config] 配置文件载入完成')
        print(f'[JustRobot]\033[32m[{_time}][INFO]\033[0m[config] Configuration load completed')

        return self._config_bot, self._config_adapter, self._config_translator, self._config_plugin

    async def update_config(self, bot, cfg, key, value):
        with open(getattr(self, f'_config_{cfg}_path'), 'r') as _f:
            _cfg = json.load(_f)

        setattr(_cfg, key, value)
        with open(getattr(self, f'_config_{cfg}_path'), 'w') as _f:
            json.dump(obj=_cfg, fp=_f, indent=2)

        # noinspection PyProtectedMember
        setattr(bot._config[cfg], key, value)

    def _initialize_config(self, path):
        _config = getattr(self, path['name'])
        _path = path['path']
        with open(_path, 'x') as _f:
            json.dump(obj=_config, fp=_f, indent=2)
