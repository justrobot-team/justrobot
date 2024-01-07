import asyncio
import os

from typing import Union


class Translator:

    def __init__(
            self,
            translators,
            bot=None
    ) -> None:
        self.translators = translators
        self.bot = bot

    async def deal(
            self,
            e
    ) -> None:

        for _, _translator in self.translators.items():

            msg_allow_deal = (
                    e.adapter in _translator.tree[_translator.name]
            ) if _translator.use_tree else True

            if _translator.matching(e) and msg_allow_deal:
                _translator.deal(e)


class Plugin:

    def __init__(
            self,
            plugins,
            log=None
    ) -> None:
        self.plugins = plugins
        self.log = log

    async def deal(
            self,
            e
    ) -> None:

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

                    self.log.error({
                        'zh': f'[{_plugin.name}] 未找到对应方法，跳过处理',
                        'en': f'[{_plugin.name}] Skipped as no corresponding method'
                    })


# noinspection PyMethodMayBeStatic
class Core:

    def __init__(
            self,
            log,
            cfg
    ) -> None:
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
        self._translators = Translator(
            translators=instances['translators'],
        )
        self._plugins = Plugin(
            plugins=instances['plugins'],
        )

    def append(
            self,
            _id,
            _client
    ) -> None:
        self.uin[_id['id']] = _id
        self.client[_id['id']] = _client

    async def deal(
            self,
            e
    ) -> None:
        if e.msg in ['/关机', '/shutdown']:
            await self.log.info('[Bot] 关机中...')
            _ = asyncio.ensure_future(self._shutdown())
            await asyncio.sleep(5)
            await self.log.info('[Bot] 关机超时，尝试强行终止进程')
            # noinspection PyProtectedMember
            os._exit(0)
        if self.translator_name_list:
            await self._translators.deal(e)
        if self.plugin_name_list:
            await self._plugins.deal(e)

    async def _shutdown(self) -> None:
        asyncio.Task.cancel(self.loop)

    @property
    def msg_recv(self) -> int:
        return self._msg_recv

    @property
    def msg_send(self) -> int:
        return self._msg_send

    def msg_recv_append(self) -> None:
        self._msg_recv += 1

    def msg_send_append(self) -> None:
        self._msg_send += 1

    def isMaster(
            self,
            adapter_name,
            user
    ) -> bool:
        try:
            return user in self._config['master'][adapter_name]
        except KeyError:
            self.log.error(f'[Bot] {adapter_name} 未配置主人')
            return False

    def get_user_list(self) -> list:
        return self._user_list

    def get_group_list(self) -> list:
        return self._group_list

    def get_guild_list(self) -> list:
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
            self.log.warn(f'[Bot]未查找到用户{uid}')
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
            self.log.warn(f'[Bot]未查找到群聊{grid}')
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
            self.log.warn(f'[Bot]未查找到子频道{cid}在服务器{guid}')
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
            self.log.warn(f'[Bot]未查找到服务器{guid}')
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
            await self.log.error(f'[Bot] {_message}')
            return False

        if isinstance(uid, list):
            if not len(uid) == 2:
                return await _error(f'uid 长度不符合要求: {len(uid)} 不是合法的 uid 长度')

            if uid[0] not in self.adapter_name_list:
                return await _error(f'适配器不存在或类型错误: {uid[0]}: {type(uid[0])}')

            if not isinstance(uid[1], str):
                return await _error(f'错误的用户 id 类型: {type(uid[1])}')

        elif isinstance(uid, (str, int, float)):
            if not adapter_name:
                return await _error('缺少参数: adapter_name')

            uid = [adapter_name, str(uid)]

        else:
            return await _error(f'uid 类型错误: {type(uid)} 不是 list, str, int, float')

        if uid in self._user_list:
            return await _error(f'不能重复添加用户 {uid[1]}')

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
            await self.log.error(f'[Bot] {_message}')
            return False

        if isinstance(grid, list):
            if not len(grid) == 2:
                return await _error(f'grid 长度不符合要求: {len(grid)} 不是合法的 grid 长度')

            if grid[0] not in self.adapter_name_list:
                return await _error(f'适配器不存在或类型错误: {grid[0]}: {type(grid[0])}')

            if not isinstance(grid[1], str):
                return await _error(f'错误的群聊 id 类型: {type(grid[1])}')

        elif isinstance(grid, (str, int, float)):
            if not adapter_name:
                return await _error('缺少参数: 适配器名称')

            grid = [adapter_name, grid]

        else:
            return await _error(f'grid 类型错误: {type(grid)} 不是 list, str, int, float')

        if grid in self._group_list:
            return await _error(f'不能重复添加群聊 {grid[1]}')

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
            await self.log.error(f'[Bot] {_message}')
            return False

        if isinstance(cid, list):
            if not len(cid) == 3:
                return await _error(f'cid 长度不符合要求: {len(cid)} 不是合法的 cid 长度')

            if cid[0] not in self.adapter_name_list:
                return await _error(f'适配器不存在或类型错误: {cid[0]}')

            if [cid[0], cid[1]] not in self._guild_list:
                return await _error(f'不能向不存在的服务器 {cid[1]} 添加子频道或类型错误')

            if not isinstance(cid[2], str):
                return await _error(f'错误的子频道 id 类型: {type(cid[2])}')

        elif isinstance(cid, (str, int, float)):
            if not guid:
                return await _error('缺少参数: 服务器名称')

            if not adapter_name:
                return await _error('缺少参数: 适配器名称')

            if not isinstance(guid, (str, int, float)):
                return await _error(f'guid 类型错误: {type(guid)} 不是 str, int, float')

            if not isinstance(adapter_name, str):
                return await _error(f'adapter_name 类型错误: {type(adapter_name)} 不是 str')

            if adapter_name not in self.adapter_name_list:
                return await _error(f'适配器不存在: {adapter_name}')

            if [adapter_name, str(guid)] not in self._guild_list:
                return await _error(f'不能向不存在的服务器 {cid[1]} 添加子频道')

            cid = [adapter_name, str(guid), cid]

        else:
            return await _error(f'cid 类型错误: {type(cid)} 不是 list, str, int. float')

        if cid in self._channel_list:
            return await _error(f'不嫩重复添加子频道 {cid[2]} 到服务器 {cid[1]}')

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
            await self.log.error(f'[Bot] {_message}')
            return False

        if isinstance(guid, list):
            if not len(guid) == 2:
                return await _error(f'guid 长度不满足要求: {len(guid)} 不是合法的guid长度')

            if guid[0] not in self.adapter_name_list:
                return await _error(f'适配器不存在或类型错误: {guid[0]}')

            if not isinstance(guid[1], str):
                return await _error(f'错误的服务器 id 类型: {type(guid[1])}')

        elif isinstance(guid, (str, int, float)):
            if not adapter_name:
                return await _error('缺少参数: 适配器名称')

            guid = [adapter_name, str(guid)]

        else:
            return await _error(f'错误的 guid 类型: {type(guid)} 不是 list, str, int. float')

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
                await self.log.error(f'[{_client.name}] 未找到方法 update_user_list')

    async def update_group_list(self) -> None:
        for _, _client in self.client.items():
            try:
                await _client.update_group_list()
            except AttributeError:
                await self.log.error(f'[{_client.name}] 未找到方法 update_group_list')

    async def update_channel_list(self) -> None:
        for _, _client in self.client.items():
            try:
                await _client.update_channel_list()
            except AttributeError:
                await self.log.error(f'[{_client.name}] 未找到方法 update_channel_list')

    async def update_guild_list(self) -> None:
        for _, _client in self.client.items():
            try:
                await _client.update_guild_list()
            except AttributeError:
                await self.log.error(f'[{_client.name}] 未找到方法 update_guild_list')
