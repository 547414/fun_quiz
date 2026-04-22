from sqlalchemy import Column, String, Boolean, Integer, Index

from basic.entity.basic_entity import BasicEntity


class MenuEntity(BasicEntity):
    __tablename__ = 'ct_menu'
    __table_args__ = (
        Index('idx_ct_menu_parent_id', 'parent_id'),
        {"comment": "菜单表"}
    )

    name = Column(String(500), nullable=False, comment='菜单名称')
    code = Column(String(500), nullable=False, comment='菜单编码')
    enabled = Column(Boolean, nullable=False, server_default='true', comment='是否启用')
    parent_id = Column(String(40), nullable=True, comment='父级菜单ID')
    url = Column(String(500), nullable=True, comment='菜单URL')
    icon = Column(String(500), nullable=True, comment='菜单图标')
    seq = Column(Integer, nullable=False, server_default='0', comment='排序')
    type = Column(String(40), nullable=False, comment='菜单类型')
