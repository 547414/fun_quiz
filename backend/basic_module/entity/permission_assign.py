import datetime

from sqlalchemy import Column, String, DateTime, text, Index, Enum

from basic.entity.basic_entity import BasicEntity
from basic_module.model.permission_assign_model import EnumPermissionAssignGrantType, EnumPermissionAssignGranteeType, \
    EnumPermissionAssignPolicy


class PermissionAssignEntity(BasicEntity):
    __tablename__ = 'ct_permission_assign'
    __table_args__ = (
        Index('idx_ct_permission_assign_grant_object_id', 'grant_object_id'),
        Index('idx_ct_permission_assign_grantee_object_id', 'grantee_object_id'),
        Index('idx_ct_permission_assign_permission_id', 'permission_id'),
        {"comment": "权限分配表"}
    )

    grant_type = Column(Enum(EnumPermissionAssignGrantType), nullable=False, comment='授权类型')
    grant_object_id = Column(String(40), nullable=False, comment='授权对象ID')
    grantee_type = Column(Enum(EnumPermissionAssignGranteeType), nullable=False, comment='被授权类型')
    grantee_object_id = Column(String(40), nullable=False, comment='被授权对象ID')
    permission_id = Column(String(40), nullable=False, comment='权限ID')
    start_time = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
        comment='授权开始时间'
    )
    policy = Column(Enum(EnumPermissionAssignPolicy), nullable=True, comment='授权策略')
    end_time = Column(DateTime(timezone=True), nullable=True, comment='授权结束时间')
