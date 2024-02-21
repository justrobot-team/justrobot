from typing import Union


# 转译器基类
# TODO: 增加一个数据库接口
# noinspection PyMethodMayBeStatic
class Translator:
    """
    中文:
    转译器基类, 用于处理事件, 从而实现初步消息处理功能.
    属性:
        name: str, 转译器名称
        event: str, 事件名称
        pri: int, 优先级
        bot: object, 机器人对象
        cfg: dict, 配置

    方法:
        load: 载入
        matching: 匹配
        deal: 处理

    English:
    Translator base class, used to process events, thus achieving preliminary message processing functions.
    Attributes:
        name: str, translator name
        event: str, event name
        pri: int, priority
        bot: object, bot object
        cfg: dict, config

    Methods:
        load: load
        matching: matching
        deal: deal
    """

    name = 'default-translater'
    event = None
    pri = 1000
    bot = None
    cfg = None

    def __init__(
            self,
            fnc_dict: list
    ) -> None:
        """
        中文:
        初始化转译器.
        :param fnc_dict: list, 函数字典
        :return: None.

        English:
        Initialize the translator.
        :param fnc_dict: list, function dictionary
        :return: None.
        """

        for key, fnc in fnc_dict:
            setattr(self, key, fnc)

    def load(
            self,
            bot: object,
            cfg: dict
    ) -> None:
        """
        中文:
        载入转译器.
        :param bot: 机器人实例
        :param cfg: 配置信息
        :return: None.

        English:
        Load the translator.
        :param bot: bot instance
        :param cfg: config
        :return: None.
        """
        self.bot = bot
        self.cfg = cfg

    def matching(
            self,
            e: object
    ) -> Union[str, bool]:
        """
        中文:
        匹配消息事件.
        :param e: 事件对象
        :return: 匹配结果

        English:
        Matching message events.
        :param e: event object
        :return: matching result
        """
        return False

    def deal(
            self,
            e: object
    ) -> None:
        """
        中文:
        处理消息事件.
        :param e: 事件对象
        :return: None.

        English:
        Processing message events.
        :param e: event object
        :return: None.
        """
        pass
