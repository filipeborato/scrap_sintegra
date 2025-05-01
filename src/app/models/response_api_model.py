from dataclasses import dataclass, field
from typing import Any, List, Dict

@dataclass
class ResponseApiModel:
    task_id: str = ''
    content: List[Any] = field(default_factory=list)
    sucesso: str = 'SIM'

    def send(self) -> Dict[str, Any]:
        return {
            "sucesso": self.sucesso,
            "task_id": self.task_id,
            "content": self.content
        }