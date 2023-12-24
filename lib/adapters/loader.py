import asyncio
import importlib
import os


class Adapter:

    def __init__(self, cfg) -> None:
        self._adapter_path = './adapters'
        self._adapters_path = []
        self.adapters = {}
        self.log = None
        self.lang = None
        self.cfg = cfg

    def _get_dir_list(self):

        _paths = os.listdir(self._adapter_path)
        for _path in _paths:
            _new_path = os.path.join(self._adapter_path, _path)
            if os.path.isdir(_new_path) and os.path.exists(os.path.join(_new_path, '__init__.py')):
                self._adapters_path.append(f'adapters.{_path}')

    async def _load_adapter(self, path):

        _load_success_log = {
            'zh': ': 适配器导入完成',
            'en': ': Adapter loaded'
        }
        _load_fail_log = {
            'zh': ': 适配器导入失败:',
            'en': ': Adapter loading failed'
        }

        try:
            _adapter = importlib.import_module(path).Adapter().load_on()
            self.adapters[_adapter.name] = _adapter
            await self.log.info('[loader] ' + _adapter.name + _load_success_log[self.lang])

        except (
                ModuleNotFoundError,
                ImportError,
                AttributeError,
                SyntaxError,
                PermissionError,
                FileNotFoundError,
                TypeError
        ) as _e:

            _lines = _e.args[0].splitlines()
            for _i in range(len(_lines)):
                if _i == 0:
                    await self.log.error(f'[loader] {path} ' + _load_fail_log[self.lang] + f': {_lines[0]}')
                else:
                    await self.log.error(_lines[_i])

    async def load(self, bot) -> dict:

        self.log = bot.log
        self.lang = bot.lang
        self._get_dir_list()

        if not self._adapters_path:
            return {}

        await asyncio.gather(*(self._load_adapter(_path) for _path in self._adapters_path))

        for _name, _adapter in self.adapters.items():
            try:
                await _adapter.load(bot, self.cfg)
            except AttributeError:
                _load_fail_log = {
                    'zh': ': 适配器导入失败，请检查是否存在编写问题',
                    'en': ': Adapter loading failed, checkout coding problem'
                }

                await self.log.error(f'[loader] {_name}{_load_fail_log[self.lang]}')

        return self.adapters
