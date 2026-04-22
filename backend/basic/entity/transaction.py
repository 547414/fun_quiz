import datetime

from sqlalchemy import Column, String, Text, text, DateTime
from sqlalchemy.dialects.postgresql import JSONB

from basic.entity.basic_entity import BasicEntity


class TransactionEntity(BasicEntity):
    __tablename__ = 'ct_transaction'
    __table_args__ = (
        {"comment": "事务表"}
    )

    current_user_info = Column(JSONB, nullable=True, comment='当前用户信息')
    start_time = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
        comment='开始时间'
    )
    end_time = Column(DateTime(timezone=True), nullable=True, comment='结束时间')
    status = Column(String(255), nullable=False, comment='状态')
    request_info = Column(JSONB, nullable=True, comment='请求信息')
    request_params = Column(JSONB, nullable=True, comment='参数')
    params = Column(JSONB, nullable=True, comment='其他参数')
