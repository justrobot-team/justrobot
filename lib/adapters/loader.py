import asyncio
import importlib
import os


# 定义一个类用于导入适配器
# Define class: load Adapters
class Adapter:
    """
    中文:
    适配器加载器, 用于导入适配器并创建适配器实例

    属性:
        adapters: 适配器实例字典
        log: 日志实例
        lang: 语言区域
        cfg: 配置信息

    私有属性:
        _adapter_path: 适配器目录
        _adapters_path: 适配器路径列表

    方法:
        load: 导入适配器实例并创建映射

    私有方法:
        _get_dir_list: 读取适配器目录, 查找有效适配器
        _load_adapter: 导入并初始化适配器

    English:
    Adapter loader, used to import adapters and create adapter instances

    Attributes:
        adapters: Adapter instance dictionary
        log: Log instance
        lang: Language region
        cfg: Configuration information

    Private attributes:
        _adapter_path: Adapter directory
        _adapters_path: Adapter path list

    Methods:
        load: Load adapters and create mapping

    Private methods:
        _get_dir_list: Read adapter directory, find valid adapters
        _load_adapter: Load and init adapters
    """

    # 初始化, 传入配置参数
    # Init and pass in configuration
    def __init__(
            self,
            cfg: dict
    ) -> None:
        """
        中文:
        初始化, 传入配置参数。
        :param cfg: 配置信息。
        :return: None

        English:
        Init and pass in configuration.
        :param cfg: Configuration information.
        :return: None.
        """
        self._adapter_path = './adapters'
        self._adapters_path = []
        self.adapters = { }
        self.log = None
        self.lang = None
        self.cfg = cfg

    # 读取适配器目录, 查找有效适配器
    # Read adapter directory, find valid adapters
    def _get_dir_list(
            self
    ) -> None:
        """
        中文:
        读取适配器目录, 查找有效适配器。
        :return: None

        English:
        Read adapter directory, find valid adapters.
        :return: None.
        """
        try:
            _paths = os.listdir(self._adapter_path)
        except FileNotFoundError:
            os.mkdir(self._adapter_path)
            return
        for _path in _paths:
            _new_path = os.path.join(self._adapter_path, _path)
            if os.path.isdir(_new_path) and os.path.exists(os.path.join(_new_path, '__init__.py')):
                self._adapters_path.append(f'adapters.{_path}')

    # 导入并初始化适配器
    # Load and init adapters
    async def _load_adapter(
            self,
            path: str
    ) -> None:
        """
        中文:
        导入并初始化适配器。
        :param path: 适配器路径。
        :return: None

        English:
        Load and init adapters.
        :param path: Adapter path.
        :return: None.
        """
        _load_success_log = [
            ': 适配器导入完成',
            ': Adapter loaded'
        ]
        _load_fail_log = [
            ': 适配器导入失败:',
            ': Adapter loading failed:'
        ]

        try:
            _adapter = importlib.import_module(path).Adapter().load_on()
            self.adapters[_adapter.name] = _adapter
            await self.log.info(
                {
                    'zh': f'[loader] {_adapter.name}{_load_success_log[0]}',
                    'en': f'[loader] {_adapter.name}{_load_success_log[1]}'
                }
            )

        except (
                ModuleNotFoundError,
                ImportError,
                AttributeError,
                SyntaxError,
                PermissionError,
                FileNotFoundError,
                TypeError
        ) as _e:

            _lines = _e.args[0].splitlines()
            for _i in range(len(_lines)):
                if _i == 0:
                    await self.log.error(
                        {
                            'zh': f'[loader] {path} ' + _load_fail_log[0] + f': {_lines[0]}',
                            'en': f'[loader] {path} ' + _load_fail_log[1] + f': {_lines[0]}'
                        }
                    )
                else:
                    await self.log.error(_lines[_i])

    # 导入适配器实例并创建映射
    # Load adapters and create mapping
    async def load(
            self,
            bot: object
    ) -> dict:
        """
        中文:
        导入适配器实例并创建映射。
        :param bot: Bot实例。
        :return: 适配器实例字典

        English:
        Load adapters and create mapping.
        :param bot: Bot instance.
        :return: Adapter instance dictionary.
        """
        self.log = bot.log
        self.lang = bot.lang
        self._get_dir_list()

        if not self._adapters_path:
            return { }

        await asyncio.gather(
            *(self._load_adapter(_path) for _path in self._adapters_path)
        )

        for _name, _adapter in self.adapters.items():
            try:
                await _adapter.load(bot, self.cfg)
            except AttributeError:
                _load_fail_log = {
                    'zh': ': 适配器导入失败，请检查是否存在编写问题',
                    'en': ': Adapter loading failed, checkout coding problem'
                }

                await self.log.error(f'[loader] {_name}{_load_fail_log[self.lang]}')

        return self.adapters
