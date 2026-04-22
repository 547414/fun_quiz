from sqlalchemy import Column, String, Boolean, INTEGER, Index, Text

from basic.entity.basic_entity import BasicEntity


class DeptEntity(BasicEntity):
    __tablename__ = 'ct_dept'
    __table_args__ = (
        Index('idx_ct_dept_organization_id', 'organization_id'),
        Index('idx_ct_dept_parent_id', 'parent_id'),
        {"comment": "部门表"}
    )

    organization_id = Column(String(40), nullable=True, comment='组织ID')
    name = Column(String(255), nullable=False, comment='部门名称')
    code = Column(String(255), nullable=False, comment='部门编码')
    category = Column(String(255), nullable=True, comment='部门类型')
    brief = Column(Text, nullable=True, comment='描述')
    parent_id = Column(String(40), nullable=True, comment='父级部门ID')
    source_category = Column(String(255), nullable=True, comment='来源类型，例如企微、钉钉等')
    source_id = Column(String(255), nullable=True, comment='来源id')
    seq = Column(INTEGER, nullable=False, default=0, comment='排序')
    enabled = Column(Boolean, nullable=False, default=True, comment='是否启用')
