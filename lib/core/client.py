from typing import Callable, Union, Dict, List

### ----------- Instance ----------- ###

'''
中文:
构建一组类用于发送消息、执行操作等

English:
Build classes for send message, took operation
'''


# 标准 user 类
# Standard 'user' class
class User:
    # 基本参数
    # Basic parameters
    id = 'default_user'
    name = id
    adapter = 'default_adapter'
    is_friend = False
    info = {
        'level': 16,
        'language': 'zh-cn',
        'first_name': name,
        'last_name': name,
        'age': 32,
        'gender': 'unknown',
        'area': 'Antarctica',
        'is_bot': False,
        'created_at': '1970-01-01 00:00:00:000',
        'display_name': id,
        'mentionable': True,
        'status': 'online',
        'activity': None
    }

    # 实例化该类, 并可选传参来快速构建
    # Instantiate this class, and optionally parameters for quickly build
    def __init__(
            self,
            info: Dict[str, Union[str, int, list]] = None
    ) -> None:
        if info:
            [setattr(self, _key, _value) for _key, _value in info.items()]

    # 传递构建完成的方法进行快速构建
    # Pass built method for quick build
    def load(
            self,
            fnc_dict: Dict[str, Callable]
    ) -> None:
        [setattr(self, _name, _fnc) for _name, _fnc in fnc_dict.items()]

    # 获取用户头像，需要返回一个url地址(web/本地)
    # Get user avatar, Return the URL address (web/local)
    async def get_avatar(
            self,
            id: str = None
    ) -> str:
        return 'file://./resources/default_img/icon.jpg'

    # 发送信息(和/或)操作, operation 需提供, msg 参数可选
    # Send message (and/or) operation, 'operation' is needed, 'msg' is optional
    async def send(self,
                   msg: List[Union[str, bytes]],
                   operation: dict = None
                   ) -> bool:
        return True


# 标准 group 类
# Standard 'group' class
class Group:
    # 基本参数
    # Basic parameters
    id = 'default_group'
    name = id
    adapter = 'default_adapter'
    info = {
        'level': 3,
        'size': 100,
        'created_at': '1971-01-01 00:00:00:000',
        'owner': '123456',
        'admin': ['1234567', '1234568']
    }

    # 实例化该类, 并可选传参来快速构建
    # Instantiate this class, and optionally parameters for quickly build
    def __init__(
            self,
            info: Dict[str, Union[str, int, list]] = None
    ) -> None:
        if info:
            [setattr(self, _key, _value) for _key, _value in info.items()]

    # 传递构建完成的方法进行快速构建
    # Pass built method for quick build
    def load(
            self,
            fnc_dict: Dict[str, Callable]
    ) -> None:
        [setattr(self, _name, _fnc) for _name, _fnc in fnc_dict.items()]

    # 获取群聊图标
    # Get group icon
    async def get_icon(self) -> str:
        return 'file://./resources/default_img/icon.jpg'

    # 获取群聊横幅(如果有，没有则用群聊图标代替)
    # Get group banners(group icon instead if none)
    async def get_banners(self) -> str:
        return self.get_icon()

    # 获取群员列表
    # Get group member list
    async def get_member_list(self) -> list:
        return []

    # 获取群员实例
    # Get group member instance
    async def pickMember(
            self,
            id: str
    ) -> User:
        return User({'id': id})

    # 发送信息(和/或)操作, operation 需提供, msg 参数可选
    # Send message (and/or) operation, 'operation' is needed, 'msg' is optional
    async def send(self,
                   msg: List[Union[str, bytes]],
                   operation: dict = None
                   ) -> bool:
        return True


# 标准 channel 类
# Standard 'channel' class
class Channel:
    # 基本参数
    # Basic parameters
    id = 'default_channel'
    name = id
    adapter = 'default_adapter'
    guild = 'default_guild'
    info = {
        'level': 3,
        'size': 100,
        'created_at': '1971-01-01 00:00:00:000',
        'owner': '123456',
        'admin': ['1234567', '1234568']
    }

    # 实例化该类, 并可选传参来快速构建
    # Instantiate this class, and optionally parameters for quickly build
    def __init__(
            self,
            info: Dict[str, Union[str, int, list]] = None
    ) -> None:
        if info:
            [setattr(self, _key, _value) for _key, _value in info.items()]

    # 传递构建完成的方法进行快速构建
    # Pass built method for quick build
    def load(
            self,
            fnc_dict: Dict[str, Callable]
    ) -> None:
        [setattr(self, _name, _fnc) for _name, _fnc in fnc_dict.items()]

    # 获取频道图标(如果有，没有则用服务器图标代替)
    # Get channel icon(guild icon instand if none)
    async def get_icon(self) -> str:
        return 'file://./resources/default_img/icon.jpg'

    # 获取频道横幅(如果有，没有则用服务器横幅代替)
    # Get channel banners(guild banners instand if none)
    async def get_banners(self) -> str:
        return self.get_icon()

    # 获取成员列表
    # Get channel member list
    async def get_member_list(self) -> List[dict]:
        return []

    # 获取成员实例
    # Get channel member instance
    async def pickMember(
            self,
            id: str
    ) -> User:
        return User({'id': id})

    # 发送信息(和/或)操作, operation 需提供, msg 参数可选
    # Send message (and/or) operation, 'operation' is needed, 'msg' is optional
    async def send(self,
                   msg: List[Union[str, bytes]],
                   operation: Dict[str, str] = None
                   ) -> bool:
        return True


# 标准 guild 类
# Standard 'guild' class
class Guild:
    # 基本参数
    # Basic parameters
    id = 'default_guild'
    name = id
    adapter = 'default_adapter'
    info = {
        'level': 3,
        'size': 100,
        'created_at': '1971-01-01 00:00:00:000',
        'owner': '123456',
        'admin': ['1234567', '1234568']
    }

    # 实例化该类, 并可选传参来快速构建
    # Instantiate this class, and optionally parameters for quickly build
    def __init__(
            self,
            info: Dict[str, Union[str, int, list]] = None
    ) -> None:
        if info:
            [setattr(self, _key, _value) for _key, _value in info.items()]

    # 传递构建完成的方法进行快速构建
    # Pass built method for quick build
    def load(
            self,
            fnc_dict: Dict[str, Callable]
    ) -> None:
        [setattr(self, _name, _fnc) for _name, _fnc in fnc_dict.items()]

    # 获取服务器图标
    # Get guild icon
    async def get_icon(self) -> str:
        return 'file://./resources/default_img/icon.jpg'

    # 获取服务器横幅(如果有, 没有则用服务器图标代替)
    # Get guild banners
    async def get_banners(self) -> str:
        return self.get_icon()

    # 获取频道列表
    # Get guild channel list
    async def get_channel_list(self) -> List:
        return []

    # 获取成员列表
    # Get guild member list
    async def get_member_list(self) -> List:
        return []

    # 获取频道实例
    # Get guild channel instance
    async def pickChannel(
            self,
            cid: str
    ) -> object:
        return Channel({'id': cid})

    # 获取成员实例
    # Get guild member instance
    async def pickMember(
            self,
            uid: str
    ) -> object:
        return User({'id': uid})


### ----------- Client ----------- ###

'''
中文:
构建一个基本的 client 实例, 用于跨频道/创建私聊等情景使用

English:
Build basic 'client' instance, for cross-channel/new DM scenarios
'''


# 提供基础的 client 实例
# Basic 'client' instance
class Baseclient:
    # 适配器名称
    # Adapter name
    adapter_name = 'default_adapter'
    adapter_version = 'default_version'
    adapter_id = 'default_id'

    # 消息收发计数
    # Msg I/O counting
    msg_recv = 0
    msg_send = 0

    def __init__(
            self,
            fnc_dict: Dict[str, Union[Callable, str]],
    ) -> None:
        # 进行方法更新
        # Update methods
        [setattr(self, _name, _fnc) for _name, _fnc in fnc_dict.items()]

    # 获取 User 实例
    # Get user instance
    def pickUser(
            self,
            uid: str,
    ) -> object:
        return User({'id': uid})

    # 获取 Group 实例
    # Get Group instance
    def pickGroup(
            self,
            grid: str
    ) -> object:
        return Group({'id': grid})

    # 获取 Channel 实例
    # Get channel instance
    def pickChannel(
            self,
            cid: str,
            guid: str = None
    ) -> object:
        return Channel({'id': cid})

    # 获取 Guild 实例
    # Get guild instance
    def pickGuild(
            self,
            guid: str
    ) -> object:
        return Guild({'id': guid})

    async def get_user_list(self) -> List[list]:
        return [['default_adapter', 'deafult_user']]

    async def get_group_list(self) -> List[list]:
        return [['default_adapter', 'deafult_group']]

    async def get_guild_list(self) -> List[list]:
        return [['default_adapter', 'deafult_guild']]

    async def update_user_list(self) -> None:
        pass

    async def update_group_list(self) -> None:
        pass

    async def update_channel_list(self) -> None:
        pass

    async def update_guild_list(self) -> None:
        pass
