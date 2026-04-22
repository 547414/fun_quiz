from sqlalchemy import Column, String, Text, Boolean, Integer, DateTime

from basic.entity.basic_entity import BasicEntity


class InviteCodeEntity(BasicEntity):
    __tablename__ = 'ct_invite_code'
    __table_args__ = (
        {"comment": "邀请码表"}
    )

    code = Column(String(500), nullable=True, comment='名称')
    brief = Column(Text, nullable=True, comment='描述')
    max_limit = Column(Integer, nullable=False, server_default='20', comment='最大限制')
    register_num = Column(Integer, nullable=False, server_default='0', comment='注册数量')
    deadline = Column(DateTime(timezone=True), nullable=True, comment='有效期')
    enabled = Column(Boolean, nullable=False, server_default='true', comment='是否启用')
    deleted = Column(Boolean, nullable=False, server_default='false', comment='是否删除')
