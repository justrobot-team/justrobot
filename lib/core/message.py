from typing import Union, Dict, List


# noinspection PyMethodMayBeStatic
class Message:
    adapter = None
    translator = None

    seq = str
    notice = str
    msg = str
    file = Union[bytes, List[bytes]]
    user = None
    group = None
    channel = None
    guild = None

    isBot = False
    isFriend = False
    isPrivate = False
    isGroup = False
    isGuild = False
    isMaster = False

    time = str

    # 初步初始化传入部分不变属性/参数/实例
    # Preliminary initialization passes in some immutable attributes/parameters/instances
    def __init__(
            self,
            parameter: dict
    ) -> None:
        [setattr(self, _key, _info) for _key, _info in parameter.items()]

    def load(
            self,
            parameter
    ) -> None:
        [setattr(self, _key, _value) for _key, _value in parameter.items()]
        if self.group and (not self.guild):
            self.isGroup = True
        if (not self.group) and self.guild:
            self.isGuild = True
        if (not self.group) and (not self.guild):
            self.isPrivate = True

    def reply(
            self,
            msg: Union[str, List[Union[str, bytes]]],
            quote: bool = False,
            operation: Union[Dict[str, int], List[int]] = None
    ) -> bool:
        return True
