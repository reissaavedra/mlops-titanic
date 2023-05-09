import os
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Protocol, Union


class DataOutputType(Enum):
    PATH = auto()
    AWS_S3 = auto()
    AZURE_BLOB = auto()


class DataOutput(Protocol):
    path: Union[Path, str] = None
    type: str

    def __allowable(self) -> bool:
        """Method to validate path's availability"""


@dataclass
class LocalPathOutput:
    path: Union[Path, str]
    type: str = DataOutputType.PATH

    def __allowable(self) -> bool:
        return os.path.isdir(self.path)
