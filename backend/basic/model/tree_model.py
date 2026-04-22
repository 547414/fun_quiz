from typing import Optional, List, TypeVar

from basic.model.basic_model import BasicModel

T = TypeVar("T", bound="TreeModel")


class TreeModel(BasicModel):
    parent_id: Optional[str] = None
    seq: int = 0
    children: Optional[List[T]] = None

    def __post_init__(self):
        if self.children is None:
            self.children = []
