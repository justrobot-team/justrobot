import asyncio
import time
from datetime import datetime
from lib.adapters.adapter import Adapter as Default


# noinspection PyMethodMayBeStatic
class Adapter:

    def __init__(self) -> None:
        self.Adapter = Default({
            'name': 'adapter_stdin',
            'id': 'stdin',
            'version': 'stdin',
            '_recv_msg': self._recv_msg,
            'reply': self.reply,
            'isFriend': self.isFriend
        })

    async def _recv_msg(self) -> dict:
        loop = asyncio.get_event_loop()
        _msg = await loop.run_in_executor(None, input, '')
        return {
            'seq': 0,
            'notice': 'text',
            'msg': _msg,
            'user': 'stdin',
            'time': time.time()
        }

    def reply(
            self,
            message
    ) -> bool:
        print(str(message.time) + ' ' + message.msg)
        return True

    def isFriend(
            self,
            user
    ) -> bool:
        return True

    def load_on(self) -> Default:
        return self.Adapter
