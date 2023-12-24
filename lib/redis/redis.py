""" 后续修改后开放 redis的 API 接口 Open this API after later change
from redis import StrictRedis
from json import dumps

class database:

    def __init__(self,
                log,
                cfg: dict = None,
                ) -> None:
        
        self.host, self.port = (cfg["ip"], cfg["port"]) if cfg else ("127.0.0.1", 6379)
        self.passwd = cfg.get("passwd", None) if cfg else None
        self.log = log
        
    
    async def load(self) -> bool:
        
        try:

            connect = StrictRedis(
                        host=self.host,
                        port=self.port,
                        password=self.passwd
                        )
        except:

            self.log.error("[redis]请检查数据库配置是否正确或是否开启")
            return False
        
        self.redis = connect
        self.log.info("[redis]数据库连接建立成功")
        return True
    
    async def register(
            self,
            uin: dict
            ):

        uin = dumps(uin)
        self.uin = uin

        try:

            await self.redis.set("bot", uin)
            self.log.info("[" + uin["name"] + "]已加载入数据库")
        
        except:

            await self.load()
            await self.redis.set("bot", uin)

        try:

            await self.redis.set(uin["name"] + "_recv", 0)
            await self.redis.set(uin["name"] + "_send", 0)

        except:

            await self.load()
            await self.redis.set(uin["name"] + "_recv", 0)
            await self.redis.set(uin["name"] + "_send", 0)
    
    async def recv_append(self):

        try:
            
            await self.redis.incr(self.uin["name"] + "_recv")
        
        except:

            await self.load()
            await self.redis.incr(self.uin["name"] + "_recv")
    
    async def send_append(self):

        try:
            
            await self.redis.incr(self.uin["name"] + "_send")
        
        except:

            await self.load()
            await self.redis.incr(self.uin["name"] + "_send")
"""
