import asyncio
import os


class Translator:

    def __init__(
            self,
            translators,
            bot=None
    ) -> None:
        self.translators = translators
        self.bot = bot

    async def deal(self, e):

        for _, _translator in self.translators.items():

            msg_allow_deal = (
                    e.adapter in _translator.tree[_translator.name]
            ) if _translator.use_tree else True

            if _translator.match(e) and msg_allow_deal:
                _translator.deal(e)


class Plugin:

    def __init__(
            self,
            plugins,
            log=None
    ) -> None:
        self.plugins = plugins
        self.log = log

    async def deal(self, e):

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

    def __init__(self, log, cfg):
        self.uin = {}
        self.client = {}
        self.log = log
        self.loop = None
        self.robot = None
        self.adapter_name_list = []
        self.translator_name_list = []
        self.plugin_name_list = []

        self._config = cfg
        self.lang = cfg['language']
        self._translators = None
        self._plugins = None
        self._msg_recv = 0
        self._msg_send = 0

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
        self.uin[_id] = _client
        self.client[_id[1]] = _client

    async def deal(self, e):
        if e.msg in ['/关机', '/shutdown']:
            await self.log.info('[Bot] 关机中...')
            _ = asyncio.ensure_future(self._shutdown())
            await asyncio.sleep(5)
            await self.log.info('[Bot] 关机超时，尝试强行终止进程')
            os._exit(0)
        if self.translator_name_list:
            await self._translators.deal(e)
        if self.plugin_name_list:
            await self._plugins.deal(e)

    async def _shutdown(self):
        asyncio.Task.cancel(self.loop)

    @property
    def msg_recv(self) -> int:
        return self._msg_recv

    @property
    def msg_send(self) -> int:
        return self._msg_send

    def msg_recv_append(self):
        self._msg_recv += 1

    def msg_send_append(self):
        self._msg_send += 1

    def isMaster(self, adapter_name, user):
        try:
            return user in self._config['master'][adapter_name]
        except KeyError:
            self.log.error(f'[Bot] {adapter_name} 未配置主人')
            return False
