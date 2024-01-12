from typing import Union


# 转译器基类
# TODO: 增加一个数据库接口
# noinspection PyMethodMayBeStatic
class Translator:
    name = 'default-translater'
    event = None
    pri = 1000
    bot = None
    cfg = None

    def __init__(
            self,
            fnc_dict
    ) -> None:
        for key, fnc in fnc_dict:
            setattr(self, key, fnc)

    def load(
            self,
            bot,
            cfg
    ) -> None:
        self.bot = bot
        self.cfg = cfg

    def matching(
            self,
            e
    ) -> Union[str, bool]:
        return False

    def deal(
            self,
            e
    ) -> None:
        pass
