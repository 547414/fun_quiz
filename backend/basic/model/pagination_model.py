from typing import List, TypeVar, Any

from pydantic import BaseModel

from basic.model.basic_model import BasisModel

T_BaseModel = TypeVar('T_BaseModel', bound=BaseModel)


class Pagination(BasisModel):
    page_index: int = 1
    page_size: int = 10
    total_count: int = 0
    filter_count: int = 0
    data: List[Any] = None

    def __post_init__(self):
        if self.children is None:
            self.children = []
