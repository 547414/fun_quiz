from typing import TypeVar, List

T = TypeVar("T", bound="TreeModel")


class TreeService:
    @staticmethod
    def build_tree(data: List[T]) -> List[T]:
        # 按 seq 字段排序 data
        data = sorted(data, key=lambda item: item.seq)

        # 创建一个字典，用于查找父节点
        lookup = {item.id: item for item in data}
        tree = []

        # 初始化每个节点的 children
        for item in data:
            item.children = []

        # 将每个节点插入到它的父节点的 children 中
        for item in data:
            parent_id = item.parent_id
            if parent_id:
                lookup[parent_id].children.append(item)
            else:
                tree.append(item)

        return tree
