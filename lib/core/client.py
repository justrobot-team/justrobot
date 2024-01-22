from typing import Callable, Dict, List, Union

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
	"""
	中文:
	用户基类

	属性:
		id: 用户 ID
		name: 用户名
		adapter: 适配器名称
		is_friend: 是否为好友
		info: 用户信息

	方法:
		load: 传递构建完成的方法进行快速构建
		get_avatar: 获取用户头像
		send: 向用户发送消息

	English:
	User base class

	Attributes:
		id: User ID
		name: Username
		adapter: Adapter name
		is_friend: Is friend
		info: User info

	Methods:
		load: Pass built method for quick build
		get_avatar: Get user avatar
		send: Send message to user
	"""
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
		"""
		中文:
		实例化该类, 并可选传参来快速构建。
		:param info: 传入用户信息(dict)。
		:return: None.

		English:
		Instantiate this class, and optionally parameters for quickly build.
		:param info: Pass user info(dict).
		:return: None.
		"""
		if info:
			[setattr(self, _key, _value) for _key, _value in info.items()]

	# 传递构建完成的方法进行快速构建
	# Pass built method for quick build
	def load(
			self,
			fnc_dict: Dict[str, Callable]
	) -> None:
		"""
		中文:
		传递构建完成的方法进行快速构建。
		:param fnc_dict: 传入的方法字典(dict)。
		:return: None.

		English:
		Pass built method for quick build.
		:param fnc_dict: Pass method dict(dict).
		:return: None.
		"""
		[setattr(self, _name, _fnc) for _name, _fnc in fnc_dict.items()]

	# 获取用户头像，需要返回一个url地址(web/本地)
	# Get user avatar, Return the URL address (web/local)
	async def get_avatar(self) -> str:
		"""
		中文:
		:return: 用户头像地址(str)。

		English:
		:return: User avatar URL(str).
		"""
		return 'file://./resources/default_img/icon.jpg'

	# 向用户发送信息
	# Send message to user
	async def send(
			self,
			e: object
	) -> bool:
		"""
		中文:
		向用户发送信息。
		:param e: 消息实例。
		:return: 消息发送是否成功(bool)。

		English:
		Send message to user.
		:param e: Message instance.
		:return: Is message send success(bool).
		"""
		return True


# 标准 group 类
# Standard 'group' class
class Group:
	"""
	中文:
	群聊基类

	属性:
		id: 群聊 ID
		name: 群聊名
		adapter: 适配器名称
		info: 群聊信息

	方法:
		load: 传递构建完成的方法进行快速构建
		get_icon: 获取群聊图标
		get_banners: 获取群聊横幅(如果有，没有则用群聊图标代替)
		get_member_list: 获取群员列表
		pickMember: 获取群员实例
		send: 向群聊发送信息

	English:
	Group base class

	Attributes:
		id: Group ID
		name: Group name
		adapter: Adapter name
		info: Group info

	Methods:
		load: Pass built method for quick build
		get_icon: Get group icon
		get_banners: Get group banners(group icon instead if none)
		get_member_list: Get group member list
		pickMember: Get group member instance
		send: Send message to group
	"""
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
		"""
		中文:
		实例化该类, 并可选传参来快速构建。
		:param info: 传入的群聊信息(dict)。
		:return: None.

		English:
		Instantiate this class, and optionally parameters for quickly build.
		:param info: Pass group info(dict).
		:return: None.
		"""
		if info:
			[setattr(self, _key, _value) for _key, _value in info.items()]

	# 传递构建完成的方法进行快速构建
	# Pass built method for quick build
	def load(
			self,
			fnc_dict: Dict[str, Callable]
	) -> None:
		"""
		中文:
		传递构建完成的方法进行快速构建。
		:param fnc_dict: 传入的方法字典(dict)。
		:return: None.

		English:
		Pass built method for quick build.
		:param fnc_dict: Pass method dict(dict).
		:return: None.
		"""
		[setattr(self, _name, _fnc) for _name, _fnc in fnc_dict.items()]

	# 获取群聊图标
	# Get group icon
	async def get_icon(self) -> str:
		"""
		中文:
		获取群聊图标。
		:return: 群聊图标地址(str)。

		English:
		Get group icon.
		:return: Group icon URL(str).
		"""
		return 'file://./resources/default_img/icon.jpg'

	# 获取群聊横幅(如果有，没有则用群聊图标代替)
	# Get group banners(group icon instead if none)
	async def get_banners(self) -> str:
		"""
		中文:
		获取群聊横幅(如果有，没有则用群聊图标代替)。
		:return: 群聊横幅地址(str)。

		English:
		Get group banners(group icon instead if none).
		:return: Group banners URL(str).
		"""
		return await self.get_icon()

	# 获取群员列表
	# Get group member list
	async def get_member_list(self) -> list:
		"""
		中文:
		获取群员列表。
		:return: 群员列表(list)。

		English:
		Get group member list.
		:return: Group member list(list).
		"""
		return []

	# 获取群员实例
	# Get group member instance
	async def pickMember(
			self,
			id: str
	) -> object:
		"""
		中文:
		:param id: 群员 ID。
		:return: 群员用户实例。

		English:
		:param id: Group member ID.
		:return: Group member user instance.
		"""
		return User({'id': id})

	# 向群聊发送信息
	# Send message to group
	async def send(
			self,
			e: object
	) -> bool:
		"""
		中文:
		向群聊发送信息。
		:param e: 消息实例。
		:return: 消息发送是否成功(bool)。

		English:
		Send message to group.
		:param e: Message instance.
		:return: Is message send success(bool).
		"""
		return True


# 标准 channel 类
# Standard 'channel' class
class Channel:
	"""
	中文:
	频道基类

	属性:
		id: 频道 ID
		name: 频道名
		adapter: 适配器名称
		guild: 服务器名称
		info: 频道信息

	方法:
		load: 传递构建完成的方法进行快速构建
		get_icon: 获取频道图标(如果有，没有则用服务器图标代替)
		get_banners: 获取频道横幅(如果有，没有则用服务器横幅代替)
		get_member_list: 获取成员列表
		pickMember: 获取成员实例
		send: 向频道发送信息

	English:
	Channel base class

	Attributes:
		id: Channel ID
		name: Channel name
		adapter: Adapter name
		guild: Guild name
		info: Channel info

	Methods:
		load: Pass built method for quick build
		get_icon: Get channel icon(guild icon instead if none)
		get_banners: Get channel banners(guild banners instead if none)
		get_member_list: Get channel member list
		pickMember: Get channel member instance
		send: Send message to channel
	"""
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
		"""
		中文:
		实例化该类, 并可选传参来快速构建。
		:param info: 传入的频道信息(dict)。
		:return: None.

		English:
		Instantiate this class, and optionally parameters for quickly build.
		:param info: Pass channel info(dict).
		:return: None.
		"""
		if info:
			[setattr(self, _key, _value) for _key, _value in info.items()]

	# 传递构建完成的方法进行快速构建
	# Pass built method for quick build
	def load(
			self,
			fnc_dict: Dict[str, Callable]
	) -> None:
		"""
		中文:
		传递构建完成的方法进行快速构建。
		:param fnc_dict: 传入的方法字典(dict)。
		:return: None.

		English:
		Pass built method for quick build.
		:param fnc_dict: Pass method dict(dict).
		:return: None.
		"""
		[setattr(self, _name, _fnc) for _name, _fnc in fnc_dict.items()]

	# 获取频道图标(如果有，没有则用服务器图标代替)
	# Get channel icon(guild icon instead if none)
	async def get_icon(self) -> str:
		"""
		中文:
		获取频道图标(如果有，没有则用服务器图标代替)。
		:return: 频道图标地址(str)。

		English:
		Get channel icon(guild icon instead if none).
		:return: Channel icon URL(str).
		"""
		return 'file://./resources/default_img/icon.jpg'

	# 获取频道横幅(如果有，没有则用服务器横幅代替)
	# Get channel banners(guild banners instead if none)
	async def get_banners(self) -> str:
		"""
		中文:
		获取频道横幅(如果有，没有则用服务器横幅代替)。
		:return: 频道横幅地址(str)。

		English:
		Get channel banners(guild banners instead if none).
		:return: Channel banners URL(str).
		"""
		return await self.get_icon()

	# 获取成员列表
	# Get channel member list
	async def get_member_list(self) -> List[dict]:
		"""
		中文:
		获取成员列表。
		:return: 成员列表(list)。

		English:
		Get channel member list.
		:return: Channel member list(list).
		"""
		return []

	# 获取成员实例
	# Get channel member instance
	async def pickMember(
			self,
			id: str
	) -> object:
		"""
		中文:
		:param id: 成员 ID。
		:return: 成员用户实例。

		English:
		:param id: Channel member ID.
		:return: Channel member user instance.
		"""
		return User({'id': id})

	# 向频道发送信息
	# Send message to channel
	async def send(
			self,
			e: object
	) -> bool:
		"""
		中文:
		向频道发送信息。
		:param e: 消息实例。
		:return: 消息发送是否成功(bool)。

		English:
		Send message to channel.
		:param e: Message instance.
		"""
		return True


# 标准 guild 类
# Standard 'guild' class
class Guild:
	"""
	中文:
	服务器基类

	属性:
		id: 服务器 ID
		name: 服务器名
		adapter: 适配器名称
		info: 服务器信息

	方法:
		load: 传递构建完成的方法进行快速构建
		get_icon: 获取服务器图标
		get_banners: 获取服务器横幅(如果有，没有则用服务器图标代替)
		get_channel_list: 获取频道列表
		get_member_list: 获取成员列表
		pickChannel: 获取频道实例
		pickMember: 获取成员实例

	English:
	Guild base class

	Attributes:
		id: Guild ID
		name: Guild name
		adapter: Adapter name
		info: Guild info

	Methods:
		load: Pass built method for quick build
		get_icon: Get guild icon
		get_banners: Get guild banners(guild icon instead if none)
		get_channel_list: Get guild channel list
		get_member_list: Get guild member list
		pickChannel: Get guild channel instance
		pickMember: Get guild member instance
	"""
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
		"""
		中文:
		实例化该类, 并可选传参来快速构建。
		:param info: 传入的服务器信息(dict)。
		:return: None.

		English:
		Instantiate this class, and optionally parameters for quickly build.
		:param info: Pass guild info(dict).
		:return: None.
		"""
		if info:
			[setattr(self, _key, _value) for _key, _value in info.items()]

	# 传递构建完成的方法进行快速构建
	# Pass built method for quick build
	def load(
			self,
			fnc_dict: Dict[str, Callable]
	) -> None:
		"""
		中文:
		传递构建完成的方法进行快速构建。
		:param fnc_dict: 传入的方法字典(dict)。
		:return: None.

		English:
		Pass built method for quick build.
		:param fnc_dict: Pass method dict(dict).
		:return: None.
		"""
		[setattr(self, _name, _fnc) for _name, _fnc in fnc_dict.items()]

	# 获取服务器图标
	# Get guild icon
	async def get_icon(self) -> str:
		"""
		中文:
		获取服务器图标。
		:return: 服务器图标地址(str)。

		English:
		Get guild icon.
		:return: Guild icon URL(str).
		"""
		return 'file://./resources/default_img/icon.jpg'

	# 获取服务器横幅(如果有, 没有则用服务器图标代替)
	# Get guild banners
	async def get_banners(self) -> str:
		"""
		中文:
		获取服务器横幅(如果有, 没有则用服务器图标代替)。
		:return: 服务器横幅地址(str)。

		English:
		Get guild banners.
		:return: Guild banners URL(str).
		"""
		return await self.get_icon()

	# 获取频道列表
	# Get guild channel list
	async def get_channel_list(self) -> List:
		"""
		中文:
		获取频道列表。
		:return: 频道列表(list)。

		English:
		Get guild channel list.
		:return: Guild channel list(list).
		"""
		return []

	# 获取成员列表
	# Get guild member list
	async def get_member_list(self) -> List:
		"""
		中文:
		获取成员列表。
		:return: 成员列表(list)。

		English:
		Get guild member list.
		:return: Guild member list(list).
		"""
		return []

	# 获取频道实例
	# Get guild channel instance
	async def pickChannel(
			self,
			cid: str
	) -> object:
		"""
		中文:
		获取频道实例。
		:param cid: 频道 ID。
		:return: 频道实例。

		English:
		Get guild channel instance.
		:param cid: Channel ID.
		:return: Channel instance.
		"""
		return Channel({'id': cid})

	# 获取成员实例
	# Get guild member instance
	async def pickMember(
			self,
			uid: str
	) -> object:
		"""
		中文:
		获取成员实例。
		:param uid: 成员 ID。
		:return: 成员实例。

		English:
		Get guild member instance.
		:param uid: Member ID.
		:return: Member instance.
		"""
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
	"""
	中文:
	适配器功能基类

	属性:
		adapter_name: 适配器名称
		adapter_version: 适配器版本
		adapter_id: 适配器ID

	私有属性:
		_msg_recv: 消息接收计数
		_msg_send: 消息发送计数

	方法:
		pickUser: 获取 User 实例
		pickGroup: 获取 Group 实例
		pickChannel: 获取 Channel 实例
		pickGuild: 获取 Guild 实例
		get_user_list: 获取用户列表
		get_group_list: 获取群聊列表
		get_guild_list: 获取服务器列表
		update_user_list: 更新用户列表
		update_group_list: 更新群聊列表
		update_channel_list: 更新频道列表
		update_guild_list: 更新服务器列表

	English:
	Adapter function base class

	Attributes:
		adapter_name: Adapter name
		adapter_version: Adapter version
		adapter_id: Adapter ID

	Private Attributes:
		_msg_recv: Message receive counting
		_msg_send: Message send counting

	Methods:
		pickUser: Get user instance
		pickGroup: Get group instance
		pickChannel: Get channel instance
		pickGuild: Get guild instance
		get_user_list: Get user list
		get_group_list: Get group list
		get_guild_list: Get guild list
		update_user_list: Update user list
		update_group_list: Update group list
		update_channel_list: Update channel list
		update_guild_list: Update guild list
	"""

	# 适配器名称
	# Adapter name
	adapter_name = 'default_adapter'
	adapter_version = 'default_version'
	adapter_id = 'default_id'

	# 消息收发计数
	# Msg I/O counting
	_msg_recv = 0
	_msg_send = 0

	def __init__(
			self,
			fnc_dict: Dict[str, Union[Callable, str]],
	) -> None:
		"""
		中文:
		实例化该类, 并可选传参来快速构建。
		:param fnc_dict: 传入的方法字典(dict)。
		:return: None.

		English:
		Instantiate this class, and optionally parameters for quickly build.
		:param fnc_dict: Pass method dict(dict).
		:return: None.
		"""
		# 进行方法更新
		# Update methods
		[setattr(self, _name, _fnc) for _name, _fnc in fnc_dict.items()]

	# 获取 User 实例
	# Get user instance
	def pickUser(
			self,
			uid: str,
	) -> object:
		"""
		中文:
		获取 User 实例。
		:param uid: 用户 ID。
		:return: 用户实例。

		English:
		Get user instance.
		:param uid: User ID.
		:return: User instance.
		"""
		return User({'id': uid})

	# 获取 Group 实例
	# Get Group instance
	def pickGroup(
			self,
			grid: str
	) -> object:
		"""
		中文:
		获取 Group 实例。
		:param grid: 群聊 ID。
		:return: 群聊实例。

		English:
		Get Group instance.
		:param grid: Group ID.
		:return: Group instance.
		"""
		return Group({'id': grid})

	# 获取 Channel 实例
	# Get channel instance
	def pickChannel(
			self,
			cid: str,
			guid: str = None
	) -> object:
		"""
		中文:
		获取 Channel 实例。
		:param cid: 频道 ID。
		:param guid: 服务器 ID。
		:return: 频道实例。

		English:
		Get channel instance.
		:param cid: Channel ID.
		:param guid: Guild ID.
		:return: Channel instance.
		"""
		return Channel({'id': cid})

	# 获取 Guild 实例
	# Get guild instance
	def pickGuild(
			self,
			guid: str
	) -> object:
		"""
		中文:
		获取 Guild 实例。
		:param guid: 服务器 ID。
		:return: 服务器实例。

		English:
		Get guild instance.
		:param guid: Guild ID.
		:return: Guild instance.
		"""
		return Guild({'id': guid})

	@property
	def msg_recv(self) -> int:
		"""
		中文:
		获取消息接收计数。
		:return: 消息接收计数(int)。

		English:
		Get message receive counting.
		:return: Message receive counting(int).
		"""
		return self._msg_recv

	@property
	def msg_send(self) -> int:
		"""
		中文:
		获取消息发送计数。
		:return: 消息发送计数(int)。

		English:
		Get message send counting.
		:return: Message send counting(int).
		"""
		return self._msg_send

	def msg_recv_append(self) -> None:
		"""
		中文:
		消息接收计数 +1。
		:return: None.

		English:
		Message receive counting +1.
		:return: None.
		"""
		self._msg_recv += 1

	def msg_send_append(self) -> None:
		"""
		中文:
		消息发送计数 +1。
		:return: None.

		English:
		Message send counting +1.
		:return: None.
		"""
		self._msg_send += 1

	async def get_user_list(self) -> List[list]:
		"""
		中文:
		获取用户列表。
		:return: 用户列表(list)。

		English:
		Get user list.
		:return: User list(list).
		"""
		return [['default_adapter', 'default_user']]

	async def get_group_list(self) -> List[list]:
		"""
		中文:
		获取群聊列表。
		:return: 群聊列表(list)。

		English:
		Get group list.
		:return: Group list(list).
		"""
		return [['default_adapter', 'default_group']]

	async def get_guild_list(self) -> List[list]:
		"""
		中文:
		获取服务器列表。
		:return: 服务器列表(list)。

		English:
		Get guild list.
		:return: Guild list(list).
		"""
		return [['default_adapter', 'default_guild']]

	async def update_user_list(self) -> None:
		"""
		中文:
		更新用户列表。
		:return: None.

		English:
		Update user list.
		:return: None.
		"""
		pass

	async def update_group_list(self) -> None:
		"""
		中文:
		更新群聊列表。
		:return: None.

		English:
		Update group list.
		"""
		pass

	async def update_channel_list(self) -> None:
		"""
		中文:
		更新频道列表。
		:return: None.

		English:
		Update channel list.
		:return: None.
		"""
		pass

	async def update_guild_list(self) -> None:
		"""
		中文:
		更新服务器列表。
		:return: None.

		English:
		Update guild list.
		:return: None.
		"""
		pass
