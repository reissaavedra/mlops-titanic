from abc import ABC, abstractmethod
from typing import List, Any


class TitanicRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Any]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Any:
        pass

    @abstractmethod
    def create(self, titanic_train: Any) -> Any:
        pass

    @abstractmethod
    def update(self, titanic_train: Any) -> Any:
        pass

    @abstractmethod
    def delete(self, titanic_train: Any) -> None:
        pass

    @abstractmethod
    def bulk_load_data(self, data: List[Any]) -> None:
        pass
