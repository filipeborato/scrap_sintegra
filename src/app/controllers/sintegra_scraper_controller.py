import secrets
import json
import re
import logging
from datetime import datetime

from models.response_api_model import ResponseApiModel
from services.producer_sintegra_goias import RabbitMQProducer
from services.redis_service import RedisService

class SintegraScraperController:
    
    async def criar_task(self, body):
        cnpj = body.get("cnpj")
        if not cnpj:
            return ResponseApiModel("", {"msg": "CNPJ is required"}, "NO").send()
        
        cnpj = re.sub(r"\D", "", cnpj)
        if len(cnpj) != 14:
            return ResponseApiModel("", {"msg": "CNPJ must have 14 digits"}, "NO").send()
        
        task_id = self.gera_task_id()
        producer = RabbitMQProducer()
        cache = RedisService()
        
        try:
            # Send message to queue
            await producer.send_message(
                "CRAWLER_CNPJ_SINTEGRA_GOIAS",
                {"task_id": task_id, "cnpj": cnpj}
            )
            # Register task in Redis
            cache.set(task_id, json.dumps({"status_task": "in_progress", "processed_data": {}}))
            return ResponseApiModel(task_id, {"status_task": "in_progress", "processed_data": {}}).send()
        except Exception as e:
            logging.exception("Error creating task:")
            return ResponseApiModel("", {"msg": "An unexpected error occurred"}, "NO").send()
        finally:
            await producer.close()
            cache.close()

    def get_task(self, task_id):
        if not task_id:
            return ResponseApiModel("", {"msg": "Task not found or invalid"}, "NO").send()
        
        cache = RedisService()
        try:
            task = cache.get(task_id)
            if task:
                return ResponseApiModel(task_id, json.loads(task)).send()
            else:
                return ResponseApiModel("", {"msg": "Task not found or invalid"}, "NO").send()
        finally:
            cache.close()
    
    def gera_task_id(self):
        random_code = secrets.token_hex(8)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{random_code}_{timestamp}"
