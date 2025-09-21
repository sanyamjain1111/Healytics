
from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseMedicalModel(ABC):
    @abstractmethod
    async def fit_and_evaluate(self, X, y) -> Dict[str, Any]:
        ...
