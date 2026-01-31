from abc import ABC, abstractmethod
from typing import Dict


class BaseLLMClient(ABC):

    @abstractmethod
    async def generate_tasks(self, prd_text: str, project_key: str) -> Dict:
        """
        Must return a dict matching TaskGenerationResponse schema.
        """
        pass
