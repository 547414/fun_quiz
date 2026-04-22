from sqlalchemy import Column, String, Boolean

from basic.entity.basic_entity import BasicEntity


class SyncLogEntity(BasicEntity):
    __tablename__ = 'ct_robot'
    __table_args__ = (
        {"comment": "同步日志表"}
    )

    name = Column(String(255), nullable=False, comment='机器人名称')
    category = Column(String(255), nullable=False, comment='机器人类型')
    enabled = Column(Boolean, nullable=False, default=True, comment='是否启用')
