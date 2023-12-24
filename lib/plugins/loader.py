import asyncio
import importlib
import os
from collections import OrderedDict


class Plugin:

    def __init__(self, cfg) -> None:
        self._plugin_path = './plugins'
        self._plugins_path = []
        self.plugins = {}
        self.cfg = cfg
        self.log = None
        self.lang = None

    def _get_dir_list(self):

        if not os.path.exists(self._plugin_path):
            os.mkdir(self._plugin_path)
        _paths = os.listdir(self._plugin_path)
        for _path in _paths:
            _new_path = os.path.join(self._plugin_path, _path)
            if os.path.isdir(_new_path) and os.path.exists(os.path.join(_new_path, '__init__.py')):
                self._plugins_path.append(f'plugins.{_path}')

    async def _load_plugin(self, path):

        _load_success_log = {
            'zh': ': 插件导入完成',
            'en': ': Plugin loaded'
        }
        _load_fail_log = {
            'zh': ': 插件导入失败:',
            'en': ': Plugin loading failed'
        }

        try:
            _plugins = importlib.import_module(path).Plugin().load_on()
            for _name, _plugin in _plugins.items():
                if not _name == 'name':
                    self.plugins[_name] = _plugin
                    await self.log.info(
                        '[loader][' + _plugins['name'] + f'][{_plugin.name}]{_load_success_log[self.lang]}'
                    )
            await self.log.info('[loader]' + _plugins['name'] + _load_success_log[self.lang])

        except (
                ModuleNotFoundError,
                ImportError,
                AttributeError,
                SyntaxError,
                PermissionError,
                FileNotFoundError,
                TypeError
        ) as _error:

            _lines = _error.args[0].splitlines()
            for _i, _line in enumerate(_lines):
                if _i == 0:
                    await self.log.error(f'[loader] {path} {_load_fail_log[self.lang]}: {_line}')
                else:
                    await self.log.error(_line)

    def _plugin_array(self):
        _list = [{'name': _name, 'plugin': _plugin} for _name, _plugin in self.plugins.items()]

        _list = sorted(_list, key=lambda _instance: _instance['plugin'].pri)

        _new_plugin = OrderedDict((_dict['name'], _dict['plugin']) for _dict in _list)

        self.plugins = _new_plugin

    async def load(self, bot):

        self.log = bot.log
        self.lang = bot.lang
        self._get_dir_list()

        if not self._plugins_path:
            return {}

        await asyncio.gather(*(self._load_plugin(_path) for _path in self._plugins_path))

        for _name, _plugin in self.plugins.items():
            try:
                _plugin.load(bot, self.cfg)
            except AttributeError:
                _load_fail_log = {
                    'zh': ': 插件导入失败，请检查是否存在编写问题',
                    'en': ': Plugin loading failed, checkout coding problem'
                }

                await self.log.error(f'[loader] {_name}{_load_fail_log[self.lang]}')

        self._plugin_array()

        return self.plugins
