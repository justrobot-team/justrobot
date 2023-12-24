import asyncio
import importlib
import os
from collections import OrderedDict


class translator:

    def __init__(self, cfg) -> None:
        self._translator_path = './translators'
        self._translators_path = []
        self.translators = {}
        self.cfg = cfg
        self.log = None
        self.lang = None

    def _get_dir_list(self):

        if not os.path.exists(self._translator_path):
            os.mkdir(self._translator_path)
        _paths = os.listdir(self._translator_path)
        for _path in _paths:
            _new_path = os.path.join(self._translator_path, _path)
            if os.path.isdir(_new_path) and os.path.exists(os.path.join(_new_path, '__init__.py')):
                self._translators_path.append(f'translators.{_path}')

    async def _load_translator(self, path):

        _load_success_log = {
            'zh': ': 转译器导入完成',
            'en': ': translator loaded'
        }
        _load_fail_log = {
            'zh': ': 转译器导入失败:',
            'en': ': translator loading failed'
        }

        try:
            _translators = importlib.import_module(path).translator().load_on()
            for _name, _translator in _translators.items():
                if not _name == 'name':
                    self.translators[_name] = _translator
                    await self.log.info(
                        '[loader][' + _translators['name'] + f'][{_translator.name}]{_load_success_log[self.lang]}'
                    )
            await self.log.info('[loader]' + _translators['name'] + _load_success_log[self.lang])

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

    def _translator_array(self):
        _list = [{'name': _name, 'translator': _translator} for _name, _translator in self.translators.items()]

        _list = sorted(_list, key=lambda _instance: _instance['translator'].pri)

        _new_translator = OrderedDict((_dict['name'], _dict['translator']) for _dict in _list)

        self.translators = _new_translator

    async def load(self, bot):

        self.log = bot.log
        self.lang = bot.lang
        self._get_dir_list()

        if not self._translators_path:
            return {}

        await asyncio.gather(*(self._load_translator(_path) for _path in self._translators_path))

        for _name, _translator in self.translators.items():
            try:
                _translator.load(bot, self.cfg)
            except AttributeError:
                _load_fail_log = {
                    'zh': ': 转译器导入失败，请检查是否存在编写问题',
                    'en': ': translator loading failed, checkout coding problem'
                }

                await self.log.error(f'[loader] {_name}{_load_fail_log[self.lang]}')

        self._translator_array()

        return self.translators