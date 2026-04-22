from sqlalchemy import Column, String, Boolean, Index, Enum

from basic.entity.basic_entity import BasicEntity
from basic_module.model.permission_model import EnumResourcePermissionCategory


class PermissionEntity(BasicEntity):
    __tablename__ = 'ct_permission'
    __table_args__ = (
        Index('idx_ct_permission_code', 'code'),
        Index('idx_ct_permission_resource_category', 'resource_category'),
        Index('idx_ct_permission_resource_id', 'resource_id'),
        {"comment": "权限表"}
    )

    name = Column(String(500), nullable=False, comment='权限名称')
    code = Column(String(500), nullable=False, comment='权限编码')
    resource_category = Column(Enum(EnumResourcePermissionCategory), nullable=False, comment='权限关联资源分类')
    resource_id = Column(String(40), nullable=False, comment='权限关联资源ID')
    enabled = Column(Boolean, nullable=False, server_default='true', comment='是否启用')
