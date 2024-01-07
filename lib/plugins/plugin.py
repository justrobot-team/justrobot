import re
from typing import Union


# 插件类的实例
# noinspection PyMethodMayBeStatic
class Plugin:
    name = 'default_plugin'
    notice = None
    event = None
    pri = 1000
    dsc = [
        {
            'reg': r'.*',
            'fnc': 'example'
        }
    ]
    bot = None
    cfg = None

    def __init__(self) -> None:
        pass

    def load(
            self,
            bot,
            cfg
    ) -> None:

        self.cfg = cfg
        self.bot = bot

    async def matching(
            self,
            e
    ) -> Union[str, bool]:

        for _reg in self.dsc:

            if re.match(re.compile(_reg['reg']), e.message):
                return _reg['fnc']

        return False

    async def example(
            self,
            e
    ) -> None:

        e.reply(e.msg)
