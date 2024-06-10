from typing import Union, Tuple, List

from dataclasses import dataclass


@dataclass
class ParseConfig:
    max_count: int
    default_tags: Union[Tuple[str], List[str]] = None
    default_count: int = 1
