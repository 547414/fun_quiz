from sqlalchemy import Column, String, Index, Boolean
from sqlalchemy.dialects.postgresql import JSONB

from basic.entity.basic_entity import BasicEntity


class UnionUserEntity(BasicEntity):
    __tablename__ = 'ct_union_user'
    __table_args__ = (
        Index('idx_ct_union_user_name', 'name'),
        {"comment": "联合用户表"}
    )

    name = Column(String(255), nullable=True, comment='名称')
    enabled = Column(Boolean, nullable=False, server_default='true', comment='是否启用')
    is_deleted = Column(Boolean, nullable=False, server_default='false', comment='是否删除')
    info = Column(JSONB, nullable=True, comment='其它信息')
