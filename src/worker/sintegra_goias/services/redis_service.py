import redis
import logging

class RedisService:
    def __init__(self, host="redis", port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.redis_client = None
        self.connect()

    def connect(self):
        try:
            self.redis_client = redis.Redis(host=self.host, port=self.port, db=self.db)
            self.redis_client.ping()
            logging.info(f"Connected to Redis at {self.host}:{self.port}")
        except Exception as e:
            logging.error(f"Error connecting to Redis: {str(e)}")

    def get(self, key):
        try:
            return self.redis_client.get(key)
        except Exception as e:
            logging.error(f"Error retrieving key {key}: {str(e)}")
            return None

    # standard expiration time: 24 hours
    def set(self, key, value, expires_in=86400):
        try:
            self.redis_client.setex(key, expires_in, value)
        except Exception as e:
            logging.error(f"Error setting key {key} with value {value}: {str(e)}")

    def close(self):
        if self.redis_client:
            self.redis_client.close()
            logging.info("Redis connection closed.")
