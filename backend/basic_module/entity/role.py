from sqlalchemy import Column, String, Boolean, Integer, Text

from basic.entity.basic_entity import BasicEntity


class RoleEntity(BasicEntity):
    __tablename__ = 'ct_role'
    __table_args__ = (
        {"comment": "角色表"}
    )

    name = Column(String(500), nullable=False, comment='角色名称')
    brief = Column(Text, nullable=True, comment='描述')
    code = Column(String(500), nullable=False, comment='角色编码')
    enabled = Column(Boolean, nullable=False, server_default='true', comment='是否启用')
    seq = Column(Integer, nullable=False, comment='排序')
