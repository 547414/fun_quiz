import datetime
from enum import Enum
from typing import Dict, Optional, Any

from pydantic import Field
from basic.model.basic_model import BasicVersionModel


class EnumTransactionStatus(Enum):
    STARTED = "STARTED"
    COMMITTED = "COMMITTED"
    ROLLED_BACK = "ROLLED_BACK"

    def __str__(self):
        labels = {
            EnumTransactionStatus.STARTED: "事务开始",
            EnumTransactionStatus.COMMITTED: "事务提交",
            EnumTransactionStatus.ROLLED_BACK: "事务回滚",
        }
        return labels[self]


class TransactionModel(BasicVersionModel):
    current_user_info: Optional[Any] = Field(None, title="Current User Info")
    start_time: Optional[datetime.datetime] = Field(None, title="Start Time")
    end_time: Optional[datetime.datetime] = Field(None, title="End Time")
    status: Optional[str] = Field(None, title="Status")
    request_info: Optional[Dict] = Field(None, title="Request Info")
    request_params: Optional[Dict] = Field(None, title="Request Params")
    params: Optional[Dict] = Field(None, title="Params")
