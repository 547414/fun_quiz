from sqlalchemy import Column, String, Boolean, INTEGER, Index

from basic.entity.basic_entity import BasicEntity


class OrganizationEntity(BasicEntity):
    __tablename__ = 'ct_organization'
    __table_args__ = (
        Index('idx_ct_organization_parent_id', 'parent_id'),
        {"comment": "组织表"}
    )

    name = Column(String(255), nullable=False, comment='组织名称')
    code = Column(String(255), nullable=False, comment='组织编码')
    category = Column(String(255), nullable=True, comment='组织类型')
    address = Column(String(500), nullable=True, comment='地址')
    parent_id = Column(String(40), nullable=True, comment='父级组织ID')
    seq = Column(INTEGER, nullable=False, default=0, comment='排序')
    enabled = Column(Boolean, nullable=False, default=True, comment='是否启用')
