import datetime

from sqlalchemy import Column, String, DateTime, Integer, Text, text, event
from sqlalchemy.orm import declared_attr

from basic import BaseEntity


class BasicEntity(BaseEntity):
    __abstract__ = True  # This makes it so this class will not be created as a table

    id = Column(String(40), primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"), index=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="创建时间"
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
        comment="更新时间"
    )
    operator = Column(String(255), nullable=True, comment="操作者")
    operator_category = Column(String(255), nullable=True, comment="操作者类别")
    version = Column(Integer, default=1, nullable=False, server_default=text("1"), comment="版本号")
    desc = Column(Text, nullable=True, comment="描述")

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


# 自动将 version 字段在每次更新时自增
@event.listens_for(BasicEntity, 'before_update', propagate=True)
def receive_before_update(mapper, connection, target):
    target.version += 1
