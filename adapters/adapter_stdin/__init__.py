import asyncio
import time
from datetime import datetime
from lib.adapters.adapter import Adapter as Default
from lib.adapters.adapter import User


# noinspection PyMethodMayBeStatic
class Adapter:

    def __init__(self) -> None:
        self.Adapter = Default({
            'name': 'stdin-adapter',
            'id': 'stdin',
            'version': 'stdin',
            '_recv_msg': self._recv_msg,
            '_send': self._send,
            'isFriend': self.isFriend,
            '_send_user': self._send_user
        })

    async def _recv_msg(self) -> dict:
        loop = asyncio.get_event_loop()
        _msg = await loop.run_in_executor(None, input, '')
        _seq = self.Adapter.client.msg_recv
        return {
            'seq': _seq,
            'notice': 'text',
            'msg': _msg,
            'file': None,
            'user': 'stdin',
            'time': str(time.time())
        }

    async def _send(
            self,
            message
    ) -> bool:
        self.Adapter.client.msg_send_append()
        print(str(message.time) + ' ' + message.msg)
        return True

    def isFriend(
            self,
            user
    ) -> bool:
        return True

    def load_on(self) -> Default:
        return self.Adapter

    async def _send_user(
            self,
            _e: object
    ) -> bool:
        self._send(_e.msg)
        return True
