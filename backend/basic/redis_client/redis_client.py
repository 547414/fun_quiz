import redis
from typing import Dict, Optional


class RedisClient:
    def __init__(self, config: Dict):
        """
        初始化 Redis 客户端
        :param config: Redis 连接配置字典
        """
        self.client = redis.StrictRedis(
            host=config["REDIS_HOST"],
            port=config.get("REDIS_PORT", 6379),
            password=config.get("REDIS_PASSWORD", None),
            db=config.get("REDIS_DB", 0),
            decode_responses=True
        )

    def set_value(self, key: str, value: str, expiration: Optional[int] = None):
        """
        设置键值，支持可选的过期时间
        :param key: 键
        :param value: 值
        :param expiration: 可选的过期时间，单位为秒
        :return: 操作结果
        """
        if expiration:
            return self.client.setex(key, expiration, value)
        return self.client.set(key, value)

    def get_value(self, key: str) -> Optional[str]:
        """
        获取键对应的值
        :param key: 键
        :return: 值，如果不存在则返回 None
        """
        return self.client.get(key)

    def delete_key(self, key: str) -> bool:
        """
        删除指定键
        :param key: 键
        :return: 如果成功删除返回 True，键不存在则返回 False
        """
        return self.client.delete(key) == 1

    def set_key_expiration(self, key: str, expiration: int) -> bool:
        """
        设置键的过期时间
        :param key: 键
        :param expiration: 过期时间，单位为秒
        :return: 如果操作成功返回 True
        """
        return self.client.expire(key, expiration)

    def exists(self, key: str) -> bool:
        """
        检查键是否存在
        :param key: 键
        :return: 存在返回 True，不存在返回 False
        """
        return self.client.exists(key) == 1

    def increment(self, key: str, amount: int = 1) -> int:
        """
        增加键对应的值
        :param key: 键
        :param amount: 增量值，默认增加 1
        :return: 增加后的值
        """
        return self.client.incr(key, amount)

    def get_ttl(self, key: str) -> int:
        """
        获取键的剩余生存时间
        :param key: 键
        :return: 剩余生存时间，单位为秒
        """
        return self.client.ttl(key)

    def flush_db(self):
        """
        清空当前 Redis 数据库
        :return: None
        """
        self.client.flushdb()
