from typing import Union, Dict, List


# noinspection PyMethodMayBeStatic
# 双工完整消息
# Full duplex complete message
class Message:
    """
    中文:
    消息类
    
    属性:
        adapter: 适配器对象
        translator: 转译器对象
        seq: 消息序列号
        notice: 消息类型
        msg: 消息内容
        file: 文件内容
        user:  User ID
        group: Group ID
        channel: Channel ID
        guild: Guild ID
        isBot: 是否为机器人
        isFriend: 是否为好友
        isPrivate: 是否为私聊
        isGroup: 是否为群聊
        isGuild: 是否为公会
        isMaster: 是否为主人
        time: 消息时间
    
    方法:
        load: 初始化消息实例
        reply: 回复消息

    English:
    Message class

    Attribute:
        adapter: Adapter object
        translator: Translator object
        seq: Message sequence number
        notice: Message type
        msg: Message content
        file: File content
        user:  User ID
        group: Group ID
        channel: Channel ID
        guild: Guild ID
        isBot: Whether it is a robot
        isFriend: Whether it is a friend
        isPrivate: Whether it is a private chat
        isGroup: Whether it is a group chat
        isGuild: Whether it is a guild
        isMaster: Whether it is the owner
        time: Message time
    
    Method:
        load: Initialize message instance
        reply: Reply message
    """

    # 存有适配器和转译器的属性
    # Attributes containing adapters and translators
    adapter: object
    translator: object

    # 消息属性
    # Message attributes
    seq: str
    notice: str
    msg: str
    file: Union[bytes, List[bytes]]
    user: Union[str, None] = None
    group: Union[str, None] = None
    channel: Union[str, None] = None
    guild: Union[str, None] = None

    # 消息情景属性
    # Message scene attributes
    isBot: bool = False
    isFriend: bool = False
    isPrivate: bool = False
    isGroup: bool = False
    isGuild: bool = False
    isMaster: bool = False

    # 消息时间属性
    # Message time attributes
    time = str

    # 初步初始化传入部分不变属性/参数/实例
    # Preliminary initialization passes in some immutable attributes/parameters/instances
    def __init__(
            self,
            parameter: dict
    ) -> None:
        """
        中文:
        构建适配器层面通用消息实例。
        :param parameter: 传入通用消息参数(dict)。
        :return: None.

        English:
        Build a common message instance at the adapter level.
        :param parameter: Pass in common message parameters(dict).
        :return: None.
        """
        [setattr(self, _key, _info) for _key, _info in parameter.items()]

    # 初始化消息实例
    # Initialize message instance
    def load(
            self,
            parameter
    ) -> None:
        """
        完成特性参数传入，构建完整消息实例。
        中文:
        :param parameter: 传入特性参数(dict)。
        :return: None.

        English:
        Finish the feature parameter pass and build a complete message instance.
        :param parameter: Pass in feature parameters(dict).
        :return: None.
        """
        [setattr(self, _key, _value) for _key, _value in parameter.items()]
        if self.group and (not self.guild):
            self.isGroup = True
        if (not self.group) and self.guild:
            self.isGuild = True
        if (not self.group) and (not self.guild):
            self.isPrivate = True

    # 回复消息
    # Reply message
    def reply(
            self,
            msg: object
    ) -> bool:
        """
        中文:
        回复消息示例方法
        :param msg: 消息实例。
        :return: 是否成功发送消息(bool)。

        English:
        Reply message example method
        :param msg: Message instance.
        :return: Whether the message was sent successfully(bool).
        """
        return True


# noinspection PyMethodMayBeStatic
# 单回复简化消息
# Single reply simplified message
class ReplyMessage:

    def __init__(
            self,
            e: object
    ) -> None:
        """
        中文:
        实例化回复消息构建类
        从 e 导入 adapter_name 和 log
        :param e: 消息实例
        :return: None

        English:
        Instantiate the reply message construction class
        Import adapter_name and log from e
        :param e: Message instance
        :return: None
        """
        # 传入参数
        # Incoming parameters
        self.msg: Union[str, None] = None
        self.file: Union[bytes, List[bytes], None] = None
        self.at_sender: bool = False
        self.notice: str = 'text'
        self.operation: Union[str, None] = None
        self.adapter_name = e.adapter_name
        self.log = e.log
        self.e = e

    # 回复消息
    # Reply message
    async def reply(
            self,
            e: object = None,
            msg: str = None,
            quote: bool = False,
            file: Union[bytes, List[bytes]] = None,
            at_sender: bool = False,
            operation: List[Dict[str, str]] = None,
    ) -> bool:
        """
        中文:
        回复消息的方法
        :param e: 异常对象
        :param msg: 消息内容
        :param quote: 是否进行回复
        :param file: 文件内容
        :param at_sender: 是否艾特发送者
        :param operation: 操作列表
        :return: 是否成功发送消息

        English:
        The method for replying to messages
        :param e: Exception object
        :param msg: Message content
        :param quote: Whether to quote
        :param file: File content
        :param at_sender: Whether to at the sender
        :param operation: Operation list
        :return: Whether the message was sent successfully
        """

        # 使用消息对象进行回复
        # Reply using message object
        if e:
            return await self.e.reply(e)

        # 发送消息
        # Send message
        if isinstance(msg, str):
            self.msg = msg
            self.at_sender = at_sender
            self.notice = 'text' if not quote else 'quote text'
            if isinstance(file, (bytes, list)):
                self.file = file
                self.notice = 'rich message' if quote else 'quote rich message'
            # 文件类型错误，应当为 bytes 或 list
            # File type error, should be bytes or list
            if file:
                self.log.warn({
                    'zh': f'[{self.adapter_name}] 文件类型错误，应当为 bytes 或 list',
                    'en': f'[{self.adapter_name}] File type error, should be bytes or list'
                })
            # 发送消息的同时不能进行操作
            # Cannot operate while sending messages
            if operation:
                self.log.warn({
                    'zh': f'[{self.adapter_name}] 发送消息的同时不能进行操作',
                    'en': f'[{self.adapter_name}] Cannot operate while sending messages'
                })
            return self.e.reply(self)

        # 消息类型错误，应当为 str
        # Message type error, should be str
        if msg and (not isinstance(msg, str)):
            self.log.error({
                'zh': f'[{self.adapter_name}] 消息类型错误，应当为 str',
                'en': f'[{self.adapter_name}] Message type error, should be str'
            })
            return False

        # 发送文件
        # Send file
        if (not msg) and isinstance(file, (bytes, list)):
            self.file = file
            self.notice = 'file' if not quote else 'quote file'
            self.at_sender = at_sender
            # 发送文件的同时不能进行操作
            # Cannot operate while sending files
            if operation:
                self.log.warn({
                    'zh': f'[{self.adapter_name}] 发送文件的同时不能进行操作',
                    'en': f'[{self.adapter_name}] Cannot operate while sending files'
                })
            return self.e.reply(self)

        # 文件类型错误，应当为 bytes 或 list
        # File type error, should be bytes or list
        if file and (not isinstance(file, (bytes, list))):
            self.log.error({
                'zh': f'[{self.adapter_name}] 文件类型错误，应当为 bytes 或 list',
                'en': f'[{self.adapter_name}] File type error, should be bytes or list'
            })
            return False

        # 进行操作
        # Perform operation
        if (not msg) and (not file):
            if operation:
                self.operation = operation
                self.notice = 'operation'
                self.log.warn({
                    'zh': f'[{self.adapter_name}] 进行操作的同时不能进行回复',
                    'en': f'[{self.adapter_name}] Cannot operate while replying'
                }) if quote else None
            if (not operation) and at_sender:
                self.at_sender = at_sender
                self.notice = 'at' if not quote else 'quote at'
            # 进行操作的同时不能进行 at
            # Cannot operate while at
            if operation and at_sender:
                self.log.warn({
                    'zh': '进行操作的同时不能进行 at',
                    'en': 'Cannot operate while at'
                })
            # 要发送消息不能为空
            # Message cannot be empty
            if (not operation) and (not at_sender):
                self.log.error({
                    'zh': f'[{self.adapter_name}] 要发送消息不能为空',
                    'en': f'[{self.adapter_name}] Message cannot be empty'
                })
                return False

            return self.e.reply(self)
