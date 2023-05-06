from abc import ABC, abstractmethod
from typing import Optional, Any


class DataExtractor(ABC):
    @abstractmethod
    def get_raw_data(self):
        """Method to extract data from source"""

    @abstractmethod
    def push_data_to_collector(self, data_collector: Optional[Any]):
        """Method to push data to collector"""
