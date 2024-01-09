import re
from typing import Union
from ..core.message import ReplyMessage

# 插件类的实例
# noinspection PyMethodMayBeStatic
class Plugin:
    
    name = 'default-plugin'
    notice: str
    event: str
    replymessage: object

    pri: int
    dsc = [
        {
            'reg': r'.*',
            'fnc': 'example'
        }
    ]
    
    bot: object
    cfg: dict

    def __init__(self) -> None:
        pass

    def load(
            self,
            bot,
            cfg
    ) -> None:

        self.cfg = cfg
        self.bot = bot
        self.replymessage = ReplyMessage
        self.log = bot.log
        self.log.info({
            'zh': f'[{self.name}] 插件已载入',
            'en': f'[{self.name}] Plugin has been loaded'
        })

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

        e.reply(
            self.replymessage(e).reply(
                msg=e.msg
            )
        )
