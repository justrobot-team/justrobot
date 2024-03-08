import re
from typing import Union

from ..core.message import ReplyMessage


# 插件基类
# TODO: 增加一个数据库接口
# noinspection PyMethodMayBeStatic
class Plugin:
    """
    中文:
    插件基类

    属性:
        name: 插件名称
        notice: 监听消息类型
        replymessage: 回复消息构建实例
        pri: 优先级
        dsc: 匹配式
        bot: 机器人实例
        cfg: 配置信息
        log: 日志实例

    方法:
        load: 插件载入
        matching: 消息匹配
        example: 示例函数

    English:
    Plugin base class

    Attribute:
        name: Plugin name
        notice: Listening message type
        replymessage: Reply message construction instance
        pri: Priority
        dsc: Matching type
        bot: Bot instance
        cfg: Configuration information
        log: Log instance

    Method:
        load: Plugin loading
        matching: Message matching
        example: Example function
    """
    # 名称
    name = 'default-plugin'
    # 监听消息类型
    notice: str
    # 回复消息构建实例
    replymessage: object

    # 优先级
    pri: int
    # 匹配式
    dsc = [
        {
            'reg': r'.*',
            'fnc': 'example'
        }
    ]

    # 机器人实例
    bot: object
    # 配置信息
    cfg: dict
    # 日志实例
    log: object

    # 初始化
    def __init__(
            self
    ) -> None:
        pass

    # 插件载入
    def load(
            self,
            bot: object,
            cfg: dict
    ) -> None:
        """
        中文:
        插件载入。
        :param bot: 机器人实例。
        :param cfg: 配置信息字典。
        :return: None.

        English:
        Plugin loading.
        :param bot: Bot instance.
        :param cfg: Configuration information dictionary.
        :return: None.
        """
        self.cfg = cfg
        self.bot = bot
        self.replymessage = ReplyMessage
        self.log = bot.log
        self.log.info(
            {
                'zh': f'[{self.name}] 插件已载入',
                'en': f'[{self.name}] Plugin has been loaded'
            }
        )

    # 消息匹配
    async def matching(
            self,
            e: object
    ) -> Union[str, bool]:
        """
        中文:
        消息匹配。
        :param e: 消息实例。
        :return: 匹配成功的函数名或无匹配结果(False)。

        English:
        Message matching.
        :param e: Message instance.
        :return: The function name of the successful match or no match result(False).
        """
        for _reg in self.dsc:

            if re.match(re.compile(_reg['reg']), e.message):
                return _reg['fnc']

        return False

    # 示例函数
    async def example(
            self,
            e: object
    ) -> bool:
        """
        中文:
        示例函数。
        :param e: 消息实例。
        :return: 是否成功(bool)。

        English:
        Example function.
        :param e: Message instance.
        :return: Whether it is successful(bool).
        """
        return await self.replymessage(e).reply(
            msg=e.msg
        )
