from sqlalchemy import Column, String, Index, Enum

from basic.entity.basic_entity import BasicEntity
from basic_module.model.user_role_model import EnumUserRoleCategory


class UserRoleEntity(BasicEntity):
    __tablename__ = 'ct_user_role'
    __table_args__ = (
        Index('idx_user_role', 'user_id', 'role_id'),
        {"comment": "用户角色表"}
    )

    user_id = Column(String(40), nullable=False, comment='用户id')
    user_category = Column(String(255), nullable=False, comment='用户类型，企微用户、web用户')
    role_id = Column(String(40), nullable=False, comment='角色id')
