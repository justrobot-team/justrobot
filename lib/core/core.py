import asyncio
import os

from typing import Union


class Translator:
    """
    中文:
    翻译器类，用于处理翻译器操作。

    属性:
        translators (dict): 包含 Translator 的字典。
        bot (可选): Bot 实例。

    方法:
        deal: 进行消息处理。
    
    English:
    Translator class for handling translation operations.

    Args:
        translators (dict): A dictionary containing translators.
        bot (optional): The bot instance.

    Methods:
        deal: Deal message.
    """

    def __init__(
            self,
            translators: dict,
            bot: object
    ) -> None:
        """
        中文:
        初始化 Translator 类。

        :param translators (字典): 包含翻译器的字典。
        :param bot (对象): 机器人实例。
        :return: None.
        
        English:
        Initializes the Translator class.

        :param translators (dict): A dictionary containing translators.
        :param bot (object): The bot instance.
        :return: None.

        """
        self.translators = translators
        self.bot = bot

    async def deal(
            self,
            e
    ) -> None:
        """
        中文:
        匹配并处理消息。

        :param e: 需要被处理的消息。

        :return: None.

        English:
        Match then deal with the message.

        :param e: The message to be dealt.

        :return: None.
        """
        for _, _translator in self.translators.items():

            msg_allow_deal = (
                    e.adapter in _translator.tree[_translator.name]
            ) if _translator.use_tree else True

            if _translator.matching(e) and msg_allow_deal:
                _translator.deal(e)


class Plugin:
    """
    中文:
    插件类，用于处理插件操作。

    属性:
        plugins (dict): 包含插件的字典。
        bot (可选): 机器人实例。

    方法:
        deal: 进行消息处理。

    English:
    Plugin class for handling plugin operations.

    Args:
        plugins (dict): A dictionary containing plugins.
        bot (optional): The robot instance.
    
    Methods:
        deal: Deal message.
    """

    def __init__(
            self,
            plugins: dict,
            bot: object
    ) -> None:
        """
        中文:
        初始化 Plugin 类。

        :param plugins: 包含插件的字典。
        :param bot: 机器人实例。
        :return: None.

        English:
        Initializes the Plugin class.

        :param plugins: A dictionary containing plugins.
        :param bot: The robot instance.
        :return: None.
        """
        self.plugins = plugins
        self.bot = bot

    async def deal(
            self,
            e
    ) -> None:
        """
        中文:
        匹配并处理消息。

        :param e: 需要被处理的消息。
        :return: None

        English:
        Match then deal with the message.

        :param e: The message to be dealt.
        :return: None
        """
        for _, _plugin in self.plugins.items():

            if hasattr(e, 'translator'):
                msg_allow_deal = (
                        (e.adapter in _plugin.tree['adapter']) and (e.translators in _plugin.tree['translator'])
                ) if _plugin.use_tree else True
            else:
                msg_allow_deal = (
                        e.adapter in _plugin.tree['adapter']
                ) if _plugin.use_tree else True

            _fnc = await _plugin.matching(e)
            if _fnc and msg_allow_deal:

                try:

                    getattr(
                        _plugin,
                        _fnc
                    )(e)

                except AttributeError:

                    self.bot.log.error({
                        'zh': f'[{_plugin.name}] 未找到对应方法，跳过处理',
                        'en': f'[{_plugin.name}] Skipped as no corresponding method'
                    })


# 机器人实例
# TODO: 增加一个数据库功能，方便适配器、转译器、插件存储数据
# noinspection PyMethodMayBeStatic
class Core:
    """
    中文:
    代表机器人的核心功能。

    属性:
        uin (字典): 用于存储用户ID及其对应信息的字典。
        client (字典): 用于存储客户端ID及其对应信息的字典。
        log: 用于记录消息的日志对象。
        loop: 用于异步操作的事件循环。
        adapter_name_list (列表): 适配器名称的列表。
        translator_name_list (列表): 翻译器名称的列表。
        plugin_name_list (列表): 插件名称的列表。
    
    私有属性:
        _config: 配置对象。 lang: 机器人使用的语言。
        _translators: 翻译器对象。
        _plugins: 插件对象。
        _msg_recv (整数): 接收到的消息数量。
        _msg_send (整数): 发送的消息数量。
        _user_list (列表): 用户ID的列表。
        _group_list (列表): 群组ID的列表。
        _channel_list (列表): 频道ID的列表。
        _guild_list (列表): 公会ID的列表。 

    方法:
        load: 加载翻译器和插件。
        append: 添加用户ID及其对应信息。
        deal: 处理消息。
        msg_recv_append: 接收到的消息数量加一。
        msg_send_append: 发送的消息数量加一。
        isMaster: 判断用户是否为主人。
        get_user_list: 获取用户ID的列表。
        get_group_list: 获取群组ID的列表。
        get_guild_list: 获取公会ID的列表。
        pickUser: 获取用户对象。
        pickGroup: 获取群组对象。
        pickChannel: 获取频道对象。
        pickGuild: 获取公会对象。
        set_user_list: 添加用户ID到列表。
        set_group_list: 添加群组ID到列表。
        set_channel_list: 添加频道ID到列表。
        set_guild_list: 添加公会ID到列表。
        update_all_list: 更新所有列表。
        update_user_list: 更新用户ID的列表。
        update_group_list: 更新群组ID的列表。
        update_channel_list: 更新频道ID的列表。
        update_guild_list: 更新公会ID的列表。
    
    私有方法:
        _shutdown: 关闭机器人。
        _set_user_list: 添加 User ID 到对应列表。
        _set_group_list: 添加 Group ID 到对应列表。
        _set_channel_list: 添加 Channel ID 到对应列表。
        _set_guild_list: 添加 Guild ID 到对应列表。
    
    English:
    Represents the core functionality of the bot.
    
    Args:
        uin (dict): The dictionary for storing user IDs and their corresponding information.
        client (dict): The dictionary for storing client IDs and their corresponding information.
        log: The logging object used for logging messages.
        loop: The event loop for asynchronous operations.
        adapter_name_list (list): The list of adapter names.
        translator_name_list (list): The list of translator names.
        plugin_name_list (list): The list of plugin names.
    
    Private Args:
        _config: The configuration object.
        _translators: The Translator object.
        _plugins: The Plugin object.
        _msg_recv (int): The number of messages received.
        _msg_send (int): The number of messages sent.
        _user_list (list): The list of user IDs.
        _group_list (list): The list of group IDs.
        _channel_list (list): The list of channel IDs.
        _guild_list (list): The list of guild IDs.
    
    Methods:
        load: Load translators and plugins.
        append: Append user ID and its corresponding information.
        deal: Deal message.
        msg_recv_append: Append the number of messages received.
        msg_send_append: Append the number of messages sent.
        isMaster: Determine whether the user is the master.
        get_user_list: Get the list of user IDs.
        get_group_list: Get the list of group IDs.
        get_guild_list: Get the list of guild IDs.
        pickUser: Get the user object.
        pickGroup: Get the group object.
        pickChannel: Get the channel object.
        pickGuild: Get the guild object.
        set_user_list: Add user ID to list.
        set_group_list: Add group ID to list.
        set_channel_list: Add channel ID to list.
        set_guild_list: Add guild ID to list.
        update_all_list: Update all lists.
        update_user_list: Update the list of user IDs.
        update_group_list: Update the list of group IDs.
        update_channel_list: Update the list of channel IDs.
        update_guild_list: Update the list of guild IDs.
    
    Private Methods:
        _shutdown: Shutdown the bot.
        _set_user_list: Add User ID to the corresponding list.
        _set_group_list: Add Group ID to the corresponding list.
        _set_channel_list: Add Channel ID to the corresponding list.
        _set_guild_list: Add Guild ID to the corresponding list.
    """

    def __init__(
            self,
            log: object,
            cfg: dict,
    ) -> None:
        """
        中文:
        初始化 Core 类。

        :param log: 用于记录消息的日志对象。
        :param cfg: 存有配置信息的字典。

        English:
        Initializes instance of the Core class.

        :param log: The logging object used for logging messages.
        :param cfg: The dictionary containing configuration information.
        """
        self.uin = {}
        self.client = {}
        self.log = log
        self.loop = None
        self.adapter_name_list = []
        self.translator_name_list = []
        self.plugin_name_list = []

        self._config = cfg
        self.lang = cfg['language']
        self._translators = None
        self._plugins = None
        self._msg_recv = 0
        self._msg_send = 0

        self._user_list = []
        self._group_list = []
        self._channel_list = []
        self._guild_list = []

    def load(
            self,
            instances
    ) -> None:
        """
        中文:
        载入导入成功的翻译器和插件。

        :param instances: 包含翻译器和插件的字典。
        :return: None.

        English:
        Load the successfully imported translators and plugins.

        :param instances: The dictionary containing translators and plugins.
        :return: None.
        """
        self._translators = Translator(
            translators=instances['translators'],
            bot=self
        )
        self._plugins = Plugin(
            plugins=instances['plugins'],
            bot=self
        )

    def append(
            self,
            _id,
            _client
    ) -> None:
        """
        中文:
        适配器注册到机器人。

        :param _id: 适配器信息。
        :param _client: 适配器对象。
        :return: None.

        English:
        Register the adapter to the bot.

        :param _id: The adapter information.
        :param _client: The adapter object.
        :return: None.
        """
        self.uin[_id['id']] = _id
        self.client[_id['id']] = _client

    async def deal(
            self,
            e
    ) -> None:
        """
        中文:
        匹配并处理消息。

        :param e: 需要被处理的消息。
        :return: None.

        English:
        Match then deal with the message.

        :param e: The message to be dealt.
        :return: None.
        """
        if e.msg in ['/关机', '/shutdown']:
            if self.isMaster(e.adapter, e.user.id):
                await self.log.info({
                    'zh': '[Bot] 关机中...',
                    'en': '[Bot] Shutting down...'
                })
                _ = asyncio.ensure_future(self._shutdown())
                await asyncio.sleep(10)
                await self.log.info({
                    'zh': '[Bot] 关机超时，尝试强行终止进程',
                    'en': '[Bot] Shutdown timeout, try to force terminate the process'
                })
                # noinspection PyProtectedMember
                os._exit(1)
            else:
                await self.log.info({
                    'zh': f'[Bot] {e.adapter} 下 {e.user} 不具有主人权限',
                    'en': f'[Bot] {e.user} under {e.adapter} does not have master permission'
                })
        if self.translator_name_list:
            await self._translators.deal(e)
        if self.plugin_name_list:
            await self._plugins.deal(e)

    async def _shutdown(self) -> None:
        """
        中文:
        向全部协程发送取消信号，等待其全部取消后关闭机器人。

        English:
        Send a cancel signal to all coroutines, wait for them to be cancelled then shut down the bot.
        """
        [_task.stop() for _task in asyncio.Task.all_tasks(self.loop)]
        exit(0)

    @property
    def msg_recv(self) -> int:
        """
        中文:
        返回接收到的消息数量。

        English:
        Return the number of messages received.
        """
        return self._msg_recv

    @property
    def msg_send(self) -> int:
        """
        中文:
        返回发送的消息数量。

        English:
        Return the number of messages sent.
        """
        return self._msg_send

    def msg_recv_append(self) -> None:
        """
        中文:
        接收到的消息数量加一。

        English:
        Append the number of messages received.
        """
        self._msg_recv += 1

    def msg_send_append(self) -> None:
        """
        中文:
        发送的消息数量加一。

        English:
        Append the number of messages sent.
        """
        self._msg_send += 1

    def isMaster(
            self,
            adapter_name,
            user
    ) -> bool:
        """
        中文:
        判断用户是否为主人。

        :param adapter_name: 适配器名称。
        :param user:  User ID。
        :return: bool.

        English:
        Determine whether the user is the master.

        :param adapter_name: The adapter name.
        :param user:  User ID.
        :return: bool.
        """
        try:
            return user in self._config['master'][adapter_name]
        except KeyError:
            asyncio.create_task(self.log.error({
                'zh': f'[Bot] {adapter_name} 不存在或未设置主人',
                'en': f'[Bot] {adapter_name} does not exist or master not set'
            }))
            return False

    def get_user_list(self) -> list:
        """
        中文:
        返回 User ID 的列表。

        :return: User ID 的列表。

        English:
        Return the list of user IDs.

        :return: The list of user IDs.
        """
        return self._user_list

    def get_group_list(self) -> list:
        """
        中文:
        返回 Group ID 的列表。

        :return: Group ID 的列表。

        English:
        Return the list of group IDs.

        :return: The list of group IDs.
        """
        return self._group_list

    def get_channel_list(self) -> list:
        """
        中文:
        返回 Channel ID 的列表。

        :return: Channel ID 的列表。

        English:
        Return the list of channel IDs.

        :return: The list of channel IDs.
        """
        return self._channel_list

    def get_guild_list(self) -> list:
        """
        中文:
        返回 Guild ID 的列表。

        :return:  Guild ID 的列表。

        English:
        Return the list of guild IDs.

        :return: The list of guild IDs.
        """
        return self._guild_list

    def pickUser(
            self,
            uid: str,
            adapter_name: str = None
    ) -> Union[object, list]:

        if adapter_name:
            _user_list = self.client[adapter_name].get_user_list()
            _user = self.client[adapter_name].pickUser(uid) if uid in _user_list else None
        else:
            _user = [self.client[_id[0]].pickUser(_id[0]) for _id in self._user_list if _id[1] == uid]

        if not _user:
            self.log.warn({
                'zh': f'[Bot]未查找到用户{uid}',
                'en': f'[Bot]User {uid} not found'
            })
            return []

        return _user

    def pickGroup(
            self,
            grid: str,
            adapter_name: str = None
    ) -> Union[object, list]:

        if adapter_name:
            _group_list = self.client[adapter_name].get_group_list()
            _group = self.client[adapter_name].pickGroup(grid) if grid in _group_list else None
        else:
            _group = [self.client[_id[0]].pickGroup(_id[0]) for _id in self._group_list if _id[1] == grid]

        if not _group:
            self.log.warn({
                'zh': f'[Bot]未查找到群聊{grid}',
                'en': f'[Bot]Group {grid} not found'
            })
            return []

        return _group

    def pickChannel(
            self,
            cid: str,
            guid: str,
            adapter_name: str = None
    ) -> Union[object, list]:

        if adapter_name:
            _channel_list = self.client[adapter_name].get_channel_list(guid)
            _channel = self.client[adapter_name].pickChannel(cid, guid) if cid in _channel_list else None
        else:
            _channel = [
                self.client[_id[0]].pickChannel(_id[0]) for _id in self._channel_list if [_id[1], _id[2]] == [guid, cid]
            ]

        if not _channel:
            self.log.warn({
                'zh': f'[Bot]未查找到子频道{cid}在服务器{guid}',
                'en': f'[Bot]Channel {cid} not found in guild {guid}'
            })
            return []

        return _channel

    def pickGuild(
            self,
            guid: str,
            adapter_name: str = None
    ) -> Union[object, list]:

        if adapter_name:
            _guild_list = self.client[adapter_name].get_guild_list()
            _guild = self.client[adapter_name].pickGuild(guid) if guid in _guild_list else None
        else:
            _guild = [self.client[_id[0]].pickUser(_id[0]) for _id in self._guild_list if _id[1] == guid]

        if not _guild:
            self.log.warn({
                'zh': f'[Bot]未查找到服务器{guid}',
                'en': f'[Bot]Guild {guid} not found'
            })
            return []

        return _guild

    def _set_user_list(
            self,
            uid
    ) -> None:
        self._user_list.append(uid)

    async def set_user_list(
            self,
            uid: Union[list, str],
            adapter_name: str = None
    ) -> bool:

        async def _error(
                _message
        ) -> bool:
            await self.log.error({
                'zh': f'[Bot] {_message[0]}',
                'en': f'[Bot] {_message[1]}'
            })
            return False

        if isinstance(uid, list):
            if not len(uid) == 2:
                return await _error([
                    f'uid 长度不符合要求: {len(uid)} 不是合法的 uid 长度',
                    f'uid length does not meet the requirements: {len(uid)} is not a valid uid length'
                ])

            if uid[0] not in self.adapter_name_list:
                return await _error([
                    f'适配器不存在或类型错误: {uid[0]}: {type(uid[0])}',
                    f'Adapter does not exist or type error: {uid[0]}: {type(uid[0])}'
                ])

            if not isinstance(uid[1], str):
                return await _error([
                    f'错误的用户 id 类型: {type(uid[1])}',
                    f'Incorrect user id type: {type(uid[1])}'
                ])

        elif isinstance(uid, (str, int, float)):
            if not adapter_name:
                return await _error([
                    '缺少参数: adapter_name',
                    'Missing parameter: adapter_name'
                ])

            uid = [adapter_name, str(uid)]

        else:
            return await _error([
                f'uid 类型错误: {type(uid)} 不是 list, str, int, float',
                f'uid type error: {type(uid)} is not list, str, int, float'
            ])

        if uid in self._user_list:
            return await _error([
                f'不能重复添加用户 {uid[1]}',
                f'Cannot add user {uid[1]} repeatedly'
            ])

        self._set_user_list(uid)
        return True

    def _set_group_list(
            self,
            grid
    ) -> None:
        self._group_list.append(grid)

    async def set_group_list(
            self,
            grid: Union[list, str],
            adapter_name: str = None
    ) -> bool:

        async def _error(
                _message
        ) -> bool:
            await self.log.error({
                'zh': f'[Bot] {_message[0]}',
                'en': f'[Bot] {_message[1]}'
            })
            return False

        if isinstance(grid, list):
            if not len(grid) == 2:
                return await _error([
                    f'grid 长度不符合要求: {len(grid)} 不是合法的 grid 长度',
                    f'grid length does not meet the requirements: {len(grid)} is not a valid grid length'
                ])

            if grid[0] not in self.adapter_name_list:
                return await _error([
                    f'适配器不存在或类型错误: {grid[0]}: {type(grid[0])}',
                    f'Adapter does not exist or type error: {grid[0]}: {type(grid[0])}'
                ])

            if not isinstance(grid[1], str):
                return await _error([
                    f'错误的群聊 id 类型: {type(grid[1])}',
                    f'Incorrect group id type: {type(grid[1])}'
                ])

        elif isinstance(grid, (str, int, float)):
            if not adapter_name:
                return await _error([
                    '缺少参数: adapter_name',
                    'Missing parameter: adapter_name'
                ])

            grid = [adapter_name, grid]

        else:
            return await _error([
                f'grid 类型错误: {type(grid)} 不是 list, str, int, float',
                f'grid type error: {type(grid)} is not list, str, int, float'
            ])

        if grid in self._group_list:
            return await _error([
                f'不能重复添加群聊 {grid[1]}',
                f'Cannot add group {grid[1]} repeatedly'
            ])

        self._set_group_list(grid)
        return True

    def _set_channel_list(
            self,
            cid
    ) -> None:
        self._channel_list.append(cid)

    async def set_channel_list(
            self,
            cid: Union[list, str],
            guid: str = None,
            adapter_name: str = None
    ) -> bool:

        async def _error(
                _message
        ) -> bool:
            await self.log.error({
                'zh': f'[Bot] {_message[0]}',
                'en': f'[Bot] {_message[1]}'
            })
            return False

        if isinstance(cid, list):
            if not len(cid) == 3:
                return await _error([
                    f'cid 长度不符合要求: {len(cid)} 不是合法的 cid 长度',
                    f'cid length does not meet the requirements: {len(cid)} is not a valid cid length'
                ])

            if cid[0] not in self.adapter_name_list:
                return await _error([
                    f'适配器不存在或类型错误: {cid[0]}',
                    f'Adapter does not exist or type error: {cid[0]}'
                ])

            if [cid[0], cid[1]] not in self._guild_list:
                return await _error([
                    f'不能向不存在的服务器 {cid[1]} 添加子频道或类型错误',
                    f'Cannot add sub-channel or type error to non-existent server {cid[1]}'
                ])

            if not isinstance(cid[2], str):
                return await _error([
                    f'错误的子频道 id 类型: {type(cid[2])}',
                    f'Incorrect channel id type: {type(cid[2])}'
                ])

        elif isinstance(cid, (str, int, float)):
            if not guid:
                return await _error([
                    '缺少参数: guild_name',
                    'Missing parameter: guild_name'
                ])

            if not adapter_name:
                return await _error([
                    '缺少参数: adapter_name',
                    'Missing parameter: adapter_name'
                ])

            if not isinstance(guid, (str, int, float)):
                return await _error([
                    f'guid 类型错误: {type(guid)} 不是 str, int, float',
                    f'guid type error: {type(guid)} is not str, int, float'
                ])

            if not isinstance(adapter_name, str):
                return await _error([
                    f'adapter_name 类型错误: {type(adapter_name)} 不是 str',
                    f'adapter_name type error: {type(adapter_name)} is not str'
                ])

            if adapter_name not in self.adapter_name_list:
                return await _error([
                    f'适配器不存在: {adapter_name}',
                    f'Adapter does not exist: {adapter_name}'
                ])

            if [adapter_name, str(guid)] not in self._guild_list:
                return await _error([
                    f'不能向不存在的服务器 {cid[1]} 添加子频道',
                    f'Cannot add sub-channel to non-existent server {cid[1]}'
                ])

            cid = [adapter_name, str(guid), cid]

        else:
            return await _error([
                f'cid 类型错误: {type(cid)} 不是 list, str, int. float',
                f'cid type error: {type(cid)} is not list, str, int. float'
            ])

        if cid in self._channel_list:
            return await _error([
                f'不嫩重复添加子频道 {cid[2]} 到服务器 {cid[1]}',
                f'Cannot add sub-channel {cid[2]} repeatedly to server {cid[1]}'
            ])

        self._set_channel_list(cid)
        return True

    def _set_guild_list(
            self,
            guid
    ) -> None:
        self._guild_list.append(guid)

    async def set_guild_list(
            self,
            guid: Union[list, str],
            adapter_name: str = None
    ) -> bool:

        async def _error(
                _message
        ) -> bool:
            await self.log.error({
                'zh': f'[Bot] {_message[0]}',
                'en': f'[Bot] {_message[1]}'
            })
            return False

        if isinstance(guid, list):
            if not len(guid) == 2:
                return await _error([
                    f'guid 长度不满足要求: {len(guid)} 不是合法的guid长度',
                    f'guid length does not meet the requirements: {len(guid)} is not a valid guid length'
                ])

            if guid[0] not in self.adapter_name_list:
                return await _error([
                    f'适配器不存在或类型错误: {guid[0]}',
                    f'Adapter does not exist or type error: {guid[0]}'
                ])

            if not isinstance(guid[1], str):
                return await _error([
                    f'错误的服务器 id 类型: {type(guid[1])}',
                    f'Incorrect guild id type: {type(guid[1])}'
                ])

        elif isinstance(guid, (str, int, float)):
            if not adapter_name:
                return await _error([
                    '缺少参数: adapter_name',
                    'Missing parameter: adapter_name'
                ])

            guid = [adapter_name, str(guid)]

        else:
            return await _error([
                f'错误的 guid 类型: {type(guid)} 不是 list, str, int. float',
                f'Incorrect guid type: {type(guid)} is not list, str, int. float'
            ])

        self._set_guild_list(guid)
        return True

    async def update_all_list(self) -> None:

        await self.update_user_list()
        await self.update_group_list()
        await self.update_channel_list()
        await self.update_guild_list()

    async def update_user_list(self) -> None:
        for _, _client in self.client.items():
            try:
                await _client.update_user_list()
            except AttributeError:
                await self.log.error({
                    'zh': f'[{_client.name}] 未找到方法 update_user_list',
                    'en': f'[{_client.name}] Method update_user_list not found'
                })

    async def update_group_list(self) -> None:
        for _, _client in self.client.items():
            try:
                await _client.update_group_list()
            except AttributeError:
                await self.log.error({
                    'zh': f'[{_client.name}] 未找到方法 update_group_list',
                    'en': f'[{_client.name}] Method update_group_list not found'
                })

    async def update_channel_list(self) -> None:
        for _, _client in self.client.items():
            try:
                await _client.update_channel_list()
            except AttributeError:
                await self.log.error({
                    'zh': f'[{_client.name}] 未找到方法 update_channel_list',
                    'en': f'[{_client.name}] Method update_channel_list not found'
                })

    async def update_guild_list(self) -> None:
        for _, _client in self.client.items():
            try:
                await _client.update_guild_list()
            except AttributeError:
                await self.log.error({
                    'zh': f'[{_client.name}] 未找到方法 update_guild_list',
                    'en': f'[{_client.name}] Method update_guild_list not found'
                })
