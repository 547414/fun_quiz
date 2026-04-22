from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSONB

from basic.entity.basic_entity import BasicEntity


class TransactionLogEntity(BasicEntity):
    __tablename__ = 'ct_transaction_log'
    __table_args__ = (
        {"comment": "事务日志表"}
    )

    transaction_id = Column(String(40), nullable=False, comment='事务ID')
    action = Column(String(255), nullable=False, comment='操作')
    params = Column(JSONB, nullable=True, comment='参数')
