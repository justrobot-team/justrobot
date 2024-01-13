import asyncio
from typing import Union

from ..core.client import Baseclient as client
from ..core.client import User, Group, Channel, Guild
from ..core.message import Message as message


# 适配器基类
# TODO: 增加一个数据库接口
# TODO: 增加一个简易构建类
# Instance Adapter
# noinspection PyMethodMayBeStatic,PyUnusedLocal
class Adapter:
    """
    中文:
    适配器基类

    属性:
        name: 适配器名称
        client: 适配器实例
        version: 适配器版本
        id: 适配器 id
        bot: bot 实例
        cfg: 适配器配置
        log: 日志实例
        basemessage: 消息实例

    方法:
        load: 导入适配器
        load_on: 类继承写法下导入类实例
        pickUser: 获取 User 实例
        pickGroup: 获取 Group 实例
        pickChannel: 获取 Channel 实例
        pickGuild: 获取 Guild 实例
        get_user_list: 获取用户列表
        get_group_list: 获取群列表
        get_channel_list: 获取频道列表
        get_guild_list: 获取服务器列表
        update_user_list: 更新用户列表
        update_group_list: 更新群列表
        update_channel_list: 更新频道列表
        update_guild_list: 更新服务器列表
        reply: 必须方法，用于调用进行消息发送
        isFriend: 判断是否为好友
        run: 具体消息接收逻辑后调用deal进行消息处理(简单示例)

    私有方法:
        _recv_msg: 接收消息的逻辑示例
        _deal: 进行消息格式转换等
        _send: 发送消息的逻辑示例
        _send_user: 发送消息给用户
        _send_group: 发送消息给群
        _send_channel: 发送消息给频道

    English:
    Instance Adapter

    Attribute:
        name: Adapter name
        client: Adapter instance
        version: Adapter version
        id: Adapter id
        bot: Bot instance
        cfg: Adapter config
        log: Log instance
        basemessage: Message instance

    Method:
        load: Loading Adapter
        load_on: Load class instance under class inheritance method
        pickUser: Get user instance
        pickGroup: Get Group instance
        pickChannel: Get channel instance
        pickGuild: Get guild instance
        get_user_list: Get user list
        get_group_list: Get group list
        get_channel_list: Get channel list
        get_guild_list: Get guild list
        update_user_list: Update user list
        update_group_list: Update group list
        update_channel_list: Update channel list
        update_guild_list: Update guild list
        reply: Must method, used to call for message sending
        isFriend: Determine whether it is a friend
        run: Example for receiving message

    Private Method:
        _recv_msg: Example for receiving message
        _deal: Translate message type
        _send: Example for sending message
        _send_user: Send message to user
        _send_group: Send message to group
        _send_channel: Send message to channel
    """

    async def _send_user(
            self,
            _e: object
    ) -> bool:
        return True

    async def _send_group(
            self,
            _e: object
    ) -> bool:
        return True

    async def _send_channel(
            self,
            _e: object
    ) -> bool:
        return True

    # 获取 User 实例
    # Get user instance
    def pickUser(
            self,
            uid: str = None
    ) -> Union[object, None]:
        if not uid:
            return None
        DefaultUser = User({
            'id': uid,
            'adapter': self.id
        })
        DefaultUser.load({
            'send': self._send_user
        })
        return DefaultUser

    # 获取 Group 实例
    # Get Group instance
    def pickGroup(
            self,
            grid: str = None
    ) -> Union[object, None]:
        if not grid:
            return None
        DefaultGroup = Group({
            'id': grid,
            'adapter': self.id
        })
        DefaultGroup.load({
            'send': self._send_group
        })
        return DefaultGroup

    # 获取 Channel 实例
    # Get channel instance
    def pickChannel(
            self,
            cid: str = None,
            guid: str = None
    ) -> Union[object, None]:
        if cid and (not guid):
            self.log.error({
                'zh': f'[{self.name}] 获取子频道实例时应传入服务器 id',
                'en': f'[{self.name}] Should pass in guild id when getting channel instance'
            })
            return None
        if (not cid) and guid:
            self.log.error({
                'zh': f'[{self.name}] 获取子频道实例时应传入子频道 id',
                'en': f'[{self.name}] Should pass in channel id when getting channel instance'
            })
            return None
        if (not cid) and (not guid):
            return None
        DefaultChannel = Channel({
            'id': cid,
            'adapter': self.id
        })
        DefaultChannel.load({
            'send': self._send_channel
        })
        return DefaultChannel

    # 获取 Guild 实例
    # Get guild instance
    def pickGuild(
            self,
            guid: str = None
    ) -> Union[object, None]:
        if not guid:
            return None
        DefaultGuild = Guild({
            'id': guid,
            'adapter': self.id
        })
        DefaultGuild.load({})
        return DefaultGuild

    def get_user_list(self) -> list:
        return [[self.name, 'default_user']]

    def get_group_list(self) -> list:
        return [[self.name, 'default_group']]

    def get_channel_list(self) -> list:
        return [[self.name, 'default_guild', 'default_channel']]

    def get_guild_list(self) -> list:
        return [[self.name, 'default_guild']]

    async def update_user_list(self) -> None:
        pass

    async def update_group_list(self) -> None:
        pass

    async def update_channel_list(self) -> None:
        pass

    async def update_guild_list(self) -> None:
        pass

    # 实例化构建
    # Instancing
    def __init__(
            self,
            cfg: dict
    ) -> None:

        # 默认参数
        # default parameters
        self.basemessage = None
        self.name = 'default-name-adapter'
        self.client = None
        self.version = 'default_version'
        self.id = 'default_id'
        self.bot = None
        self.cfg = None
        self.log = None

        # 根据传入配置信息更新属性
        # Update properties by passed config
        for key, value in cfg.items():
            setattr(self, key, value)

    # 导入适配器
    # Loading Adapter
    async def load(
            self,
            bot: object,
            cfg: dict
    ) -> None:
        self.cfg = cfg
        self.bot = bot
        self.log = bot.log

        _uin = {
            'name': self.name,
            'id': self.id,
            'version': self.version
        }

        self.client = client({
            'adapter_name': self.name,
            'adapter_id': self.id,
            'adapter_version': self.version,
            'pickUser': self.pickUser,
            'pickGroup': self.pickGroup,
            'pickChannel': self.pickChannel,
            'pickGuild': self.pickGuild,
            'get_user_list': self.get_user_list,
            'get_group_list': self.get_group_list,
            'get_channel_list': self.get_channel_list,
            'get_guild_list': self.get_guild_list,
            'update_user_list': self.update_user_list,
            'update_group_list': self.update_group_list,
            'update_channel_list': self.update_channel_list,
            'update_guild_list': self.update_guild_list
        })

        self.bot.append(_uin, self.client)

        self.basemessage = message({
            "adapter": self.name,
            "bot": self.bot
        })

    # 类继承写法下导入类实例
    # Load class instance under class inheritance method
    def load_on(self) -> object:
        return self

    # 接收消息的逻辑示例
    # Example for receiving message
    async def _recv_msg(self) -> dict:
        return {}

    # 进行消息格式转换等
    # Translate message type
    async def _deal(
            self,
            _message: dict
    ) -> None:
        self.client.msg_recv_append()
        adapter_name_initial = self.name.replace('-adapter', '')
        await self.log.info({
            'zh': f'[{adapter_name_initial}] 收到消息: ' + _message['msg'],
            'en': f'[{adapter_name_initial}] Message received: ' + _message['msg']
        })
        e = self.basemessage

        e.load({
            'adapter': self.name,
            'seq': _message.get("seq"),
            'notice': _message.get('notice'),
            'msg': _message.get('msg'),
            'file': _message.get('file'),
            'isFriend': self.isFriend(_message.get('user')),
            'isMaster': self.bot.isMaster(self.name, _message.get('user')),
            'user': self.client.pickUser(_message.get('user')),
            "group": self.client.pickGroup(_message.get('group')),
            'channel': self.client.pickChannel(_message.get('channel'), _message.get('guild')),
            'guild': self.client.pickGuild(_message.get('guild')),
            "time": _message.get('time'),
            'reply': self.reply
        })
        try:
            await self.bot.deal(e)
        except SystemExit:
            exit()

    async def _send(
            self,
            _e: object
    ) -> bool:
        self.client.msg_send_append()
        return True

    # 必须方法，用于调用进行消息发送
    async def reply(
            self,
            _e: object
    ) -> bool:
        return await self._send(_e)

    def isFriend(
            self,
            user: str
    ) -> bool:
        return False

    # 具体消息接收逻辑后调用deal进行消息处理(简单示例)
    async def run(self) -> None:
        # 简单示例
        # Simple example
        while True:
            msg = await self._recv_msg()

            try:
                _ = asyncio.create_task(self._deal(msg))
            except SystemExit:
                exit()
