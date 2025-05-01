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
            return ResponseApiModel("", {"msg": "CNPJ é obrigatório"}, "NAO").send()
        
        cnpj = re.sub(r"\D", "", cnpj)
        if len(cnpj) != 14:
            return ResponseApiModel("", {"msg": "CNPJ deve ter 14 dígitos"}, "NAO").send()
        
        task_id = self.gera_task_id()
        producer = RabbitMQProducer()
        cache = RedisService()
        
        try:
            # Envia a mensagem para a fila
            await producer.send_message(
                "CRAWLER_CNPJ_SINTEGRA_GOIAS",
                {"task_id": task_id, "cnpj": cnpj}
            )
            # Registra a task no Redis
            cache.set(task_id, json.dumps({"status_task": "em_andamento", "dados_processados": {}}))
            return ResponseApiModel(task_id, {"status_task": "em_andamento", "dados_processados": {}}).send()
        except Exception as e:
            logging.exception("Erro ao criar task:")
            return ResponseApiModel("", {"msg": "Ocorreu um erro inesperado"}, "NAO").send()
        finally:
            await producer.close()
            cache.close()

    def get_task(self, task_id):
        if not task_id:
            return ResponseApiModel("", {"msg": "Task não encontrada ou inválida"}, "NAO").send()
        
        cache = RedisService()
        try:
            task = cache.get(task_id)
            if task:
                return ResponseApiModel(task_id, json.loads(task)).send()
            else:
                return ResponseApiModel("", {"msg": "Task não encontrada ou inválida"}, "NAO").send()
        finally:
            cache.close()
    
    def gera_task_id(self):
        random_code = secrets.token_hex(8)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{random_code}_{timestamp}"
