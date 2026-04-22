from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.dialects.postgresql import JSONB

from basic.entity.basic_entity import BasicEntity


class UserEntity(BasicEntity):
    __tablename__ = 'ct_web_user'
    __table_args__ = (
        {"comment": "用户表"}
    )

    name = Column(String(500), nullable=False, comment='用户名称')
    mobile = Column(String(255), nullable=True, comment='手机号')
    email = Column(String(255), nullable=True, comment='邮箱')
    enabled = Column(Boolean, nullable=False, server_default='true', comment='是否启用')
    avatar_file_info = Column(JSONB, nullable=True, comment='头像文件信息')
    password_salt = Column(String(255), nullable=False, comment='密码盐')
    password_hash = Column(String(500), nullable=False, comment='密码')
    try_count = Column(Integer, nullable=False, server_default='0', comment='登录失败次数')
    reset_password = Column(Boolean, nullable=False, server_default='false', comment='是否重置密码')
