import os
from datetime import datetime
from typing import Union, Dict


# 打印日志
# Print log
class Log:
    """
    中文:
    打印日志

    属性:
        level: 日志级别
        path: 日志路径
        lang: 日志语言

    方法:
        debug: debug 等级日志
        info: info 等级日志
        warn: warning 等级日志
        error: error 等级日志
        fatal: fatal 等级日志

    English:
    Print log

    Attributes:
        level: Log level
        path: Log path
        lang: Log language

    Methods:
        debug: Log level debug
        info: Log level info
        warn: Log level warning
        error: Log level error
        fatal: Log level fatal
    """
    # 日志级别
    DEBUG = 5
    INFO = 4
    WARN = 3
    ERROR = 2
    FATAL = 1

    # 日志颜色 ANSI 转译码
    # Log color by ANSI
    color = {
        'msg': '\033[0m',
        'DEBUG': '\033[34m',
        'INFO': '\033[32m',
        'WARN': '\033[33m',
        'ERROR': '\033[31m',
        'FATAL': '\033[31m'
    }

    # 初始化
    # Initialize
    def __init__(
            self,
            cfg: dict
    ) -> None:
        """
        中文:
        初始化日志实例。
        :param cfg: 配置信息。
        :return: None.

        English:
        Initialize log instance.
        :param cfg: Config.
        :return: None.
        """
        self.level = cfg['level']
        self.path = os.path.join(os.getcwd(), "log")
        self.lang = cfg['lang']

        os.makedirs(self.path, exist_ok=True)

    # 写入日志
    # Write logs
    async def _write_log(
            self,
            time: str,
            msg: str
    ) -> None:
        """
        中文:
        日志写入到日志文件。
        :param time: 日志时间。
        :param msg: 日志内容。
        :return: None.

        English:
        Write logs to log file.
        :param time: Log time.
        :param msg: Log content.
        :return: None.
        """
        with open(os.path.join(self.path, f'{time}.log'), 'a', encoding='utf-8') as log_file:
            log_file.write(msg)
            log_file.write('\n')

    # 打印并写入日志
    # Print & write logs
    async def _log(
            self,
            level: str,
            msg: Union[Dict[str, str], str]
    ) -> None:
        """
        中文:
        打印并写入日志。
        :param level: 日志等级。
        :param msg: 日志内容。
        :return: None.

        English:
        Print & write logs.
        :param level: Log level.
        :param msg: Log content.
        :return: None.
        """

        # 解析字典类型的日志内容
        def _get_msg(
                _msg: dict
        ) -> str:
            """
            中文:
            解析字典类型的日志内容。
            :param _msg: 日志内容。
            :return: 解析后的日志内容。

            English:
            Parse log content of dict type.
            :param _msg: Log content.
            :return: Parsed log content.
            """
            try:
                return _msg.get(self.lang, msg['en'])
            except KeyError:
                return _msg[next(iter(msg))]

        _msg = _get_msg(msg) if isinstance(msg, dict) else msg

        if self.level >= getattr(self, level):
            _time = datetime.now().strftime("%H:%M:%S:%f")[:-3]
            write_log = f'[JustRobot][{_time}][{level}]{_msg}'
            print_log = '[JustRobot]' + self.color[level] + f'[{_time}][{level}]' + self.color['msg'] + _msg

            print(print_log)
            await self._write_log(datetime.now().strftime('%Y-%m-%d'), write_log)

    # debug 等级
    # Level debug
    async def debug(
            self,
            msg: Union[Dict[str, str], str]
    ) -> None:
        """
        中文:
        Debug 等级日志。
        :param msg: 日志内容。
        :return: None.

        English:
        Log level debug.
        :param msg: Log content.
        :return: None.
        """
        await self._log('DEBUG', msg)

    # info 等级
    # Level info
    async def info(
            self,
            msg: Union[Dict[str, str], str]
    ) -> None:
        """
        中文:
        Info 等级日志。
        :param msg: 日志内容。
        :return: None.

        English:
        Log level info.
        :param msg: Log content.
        :return: None.
        """
        await self._log('INFO', msg)

    # warning 等级
    # Level warning
    async def warn(
            self,
            msg: Union[Dict[str, str], str]
    ) -> None:
        """
        中文:
        Warning 等级日志。
        :param msg: 日志内容。
        :return: None.

        English:
        Log level warning.
        :param msg: Log content.
        :return: None.
        """
        await self._log('WARN', msg)

    # error 等级
    # Level error
    async def error(
            self,
            msg: Union[Dict[str, str], str]
    ) -> None:
        """
        中文:
        Error 等级日志。
        :param msg: 日志内容。
        :return: None.

        English:
        Log level error.
        :param msg: Log content.
        :return: None.
        """
        await self._log('ERROR', msg)

    # fatal 等级
    # Level fatal
    async def fatal(
            self,
            msg: Union[Dict[str, str], str]
    ) -> None:
        """
        中文:
        Fatal 等级日志。
        :param msg: 日志内容。
        :return: None.

        English:
        Log level fatal.
        :param msg: Log content.
        :return: None.
        """
        await self._log('FATAL', msg)
