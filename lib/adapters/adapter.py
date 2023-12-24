import asyncio

from ..core.client import Baseclient as client
from ..core.client import User, Group, Channel, Guild
from ..core.message import Message as message


# 适配器类
# Instance Adapter
# noinspection PyMethodMayBeStatic,PyUnusedLocal
class Adapter:

    # 获取 User 实例
    # Get user instance
    def pickUser(
            self,
            uid: str,
    ) -> User:
        return User({'id': uid})

    # 获取 Group 实例
    # Get Group instance
    def pickGroup(
            self,
            grid: str
    ) -> Group:
        return Group({'id': grid})

    # 获取 Channel 实例
    # Get channel instance
    def pickChannel(
            self,
            cid: str,
            guid: str = None
    ) -> Channel:
        return Channel({'id': cid})

    # 获取 Guild 实例
    # Get guild instance
    def pickGuild(
            self,
            guid: str
    ) -> Guild:
        return Guild({'id': guid})

    # 实例化构建
    # Instancing
    def __init__(
            self,
            cfg: dict
    ) -> None:

        # 默认参数
        # default parameters
        self.basemessage = None
        self.name = 'default_adapter_name'
        self.client = None
        self.version = 'default_version'
        self.id = 'default_id'
        self.bot = None
        self.cfg = None
        self.log = None

        # 根据传入配置信息更新属性
        # Update properties by passed configuration information
        for key, value in cfg.items():
            setattr(self, key, value)

    # 导入适配器
    # Loading Adapter
    async def load(
            self,
            bot,
            cfg
    ):
        self.cfg = cfg
        self.bot = bot
        self.log = bot.log

        uin = (
            self.name,
            self.id,
            self.version
        )

        self.client = client({
            'adapter_name': self.name,
            'adapter_id': self.id,
            'adapter_version': self.version,
            'pickUser': self.pickUser,
            'pickGroup': self.pickGroup,
            'pickChannel': self.pickChannel,
            'pickGuild': self.pickGuild
        })

        self.bot.append(uin, self.client)

        self.basemessage = message({
            "adapter": self.name,
            "bot": self.bot
        })

    # 接收消息的逻辑示例
    # Example for receiving message
    async def _recv_msg(self):
        return {}

    # 进行消息格式转换等
    # Translate message type
    async def _deal(
            self,
            _message
    ):
        await self.log.info('[stdin] 收到消息: ' + _message['msg'])
        e = self.basemessage

        e.load({
            'adapter': self.name,
            'seq': _message["seq"],
            'notice': _message['notice'],
            'msg': _message["msg"],
            'isFriend': self.isFriend(_message['user']),
            'isMaster': self.bot.isMaster(self.name, _message['user']),
            'user': self.client.pickUser(_message["user"]),
            "group": self.client.pickGroup(_message.get('group')),
            'channel': self.client.pickChannel(_message.get('channel')),
            'guild': self.client.pickGuild(_message.get('guild')),
            "time": _message["time"],
            'reply': self.reply
        })

        await self.bot.deal(e)

    # 必须方法，用于调用进行消息发送
    async def reply(
            self,
            _message: message
    ) -> bool:
        return True

    def isFriend(self, user):
        return False

    # 具体消息接收逻辑后调用deal进行消息处理(简单示例)
    async def run(self) -> None:
        # 简单示例
        # Simple example
        while True:

            try:
                msg = await self._recv_msg()

                _ = asyncio.create_task(self._deal(msg))

            except asyncio.CancelledError:

                await self.log.info(f'[{self.name}] 协程被取消')
