import os
from datetime import datetime


# 打印日志
# Print log
class Log:
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
            cfg
    ) -> None:
        self.level = cfg['level']
        self.path = os.path.join(os.getcwd(), "log")
        self.lang = cfg['lang']

        os.makedirs(self.path, exist_ok=True)

    # 写入日志
    # Write logs
    async def _write_log(
            self,
            time,
            msg
    ) -> None:
        with open(os.path.join(self.path, f'{time}.log'), 'a', encoding='utf-8') as log_file:
            log_file.write(msg)
            log_file.write('\n')

    # 打印并写入日志
    # Print & write logs
    async def _log(
            self,
            level,
            msg
    ) -> None:

        def _get_msg(
                _msg: dict
                ) -> str:
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
            msg
    ) -> None:
        await self._log('DEBUG', msg)

    # info 等级
    # Level info
    async def info(
            self,
            msg
    ) -> None:
        await self._log('INFO', msg)

    # warning 等级
    # Level warning
    async def warn(
            self,
            msg
    ) -> None:
        await self._log('WARN', msg)

    # error 等级
    # Level error
    async def error(
            self,
            msg
    ) -> None:
        await self._log('ERROR', msg)

    # fatal 等级
    # Level fatal
    async def fatal(
            self,
            msg
    ) -> None:
        await self._log('FATAL', msg)
