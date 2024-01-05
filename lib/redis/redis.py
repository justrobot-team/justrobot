import asyncio

import redis
from redis import StrictRedis, ConnectionPool


class Database:

    def __init__(self,
                 bot,
                 cfg: dict = None,
                 ) -> None:

        self.host, self.port = (cfg["ip"], cfg["port"]) if cfg else ("127.0.0.1", 6379)
        self.passwd = cfg.get("passwd", None) if cfg else None
        self.log = bot.log
        self._pool = None
        self.redis = None

    async def _connect(self) -> bool:
        _pool = ConnectionPool(
            host=self.host,
            port=self.port,
            password=self.passwd,
            db=0,
            timeout=5
        )

        self._pool = _pool
        await self.log.info("[redis] 连接初始化完成")
        try:
            with StrictRedis(self._pool) as _connect:
                _connect.close()
        except redis.ConnectionError:
            self.log.error('[redis] 连接失败，请检查 redis 数据库状态')
        except redis.TimeoutError:
            self.log.error('[redis] 数据库连接超时，请检查是否已开启 redis')
        return True

    async def load(self) -> bool:
        for _freq in range(1, 5):
            _back = await self._connect()
            if _back:
                return True

            else:
                await self.log.error(f'[redis] 连接失败，第{_freq}次重试...')
                await asyncio.sleep(3)
