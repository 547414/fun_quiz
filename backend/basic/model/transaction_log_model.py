from enum import Enum

from pydantic import Field
from typing import Dict, Optional

from basic.model.basic_model import BasicVersionModel


class EnumTransactionLogAction(Enum):
    STARTED = "STARTED"
    COMMITTED = "COMMITTED"
    ROLLED_BACK = "ROLLED_BACK"
    ENDED = "ENDED"

    def __str__(self):
        labels = {
            EnumTransactionLogAction.STARTED: "事务开始",
            EnumTransactionLogAction.COMMITTED: "事务提交",
            EnumTransactionLogAction.ROLLED_BACK: "事务回滚",
            EnumTransactionLogAction.ENDED: "事务结束",
        }
        return labels[self]


class TransactionLogModel(BasicVersionModel):
    transaction_id: Optional[str] = Field(None, title="Transaction ID")
    action: Optional[str] = Field(None, title="Action")
    params: Optional[Dict] = Field(None, title="Params")
