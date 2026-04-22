import datetime
import uuid
from contextlib import contextmanager
from typing import Dict, TypeVar, Type

from pydantic import BaseModel

from basic import BaseEntity
from basic.entity.transaction import TransactionEntity
from basic.entity.transaction_log import TransactionLogEntity
from basic.model.fastapi_request_for_log_model import FastApiRequestForLogModel
from basic.model.transaction_log_model import TransactionLogModel, EnumTransactionLogAction
from basic.model.transaction_model import TransactionModel, EnumTransactionStatus
from basic.repository.base_repository import BaseRepository

T_BaseModel = TypeVar('T_BaseModel', bound=BaseModel)
U_BaseEntity = TypeVar('U_BaseEntity', bound=BaseEntity)


class UnitOfWork:
    def __init__(
            self,
            session_factory,
            current_user_info: Dict = None,
            request_info: FastApiRequestForLogModel = None,
            request_params: Dict = None,
            params: Dict = None
    ):
        self.session_factory = session_factory
        self.session = None
        self.current_user_info = current_user_info
        self.request_info = request_info
        self.request_params = request_params
        self.params = params
        self._transaction_id = None
        self._base_repository = BaseRepository(session_factory)

    def init_log_data(
            self,
            current_user_info: Dict = None,
            request_info: FastApiRequestForLogModel = None,
            request_params: Dict = None,
            params: Dict = None
    ):
        self.current_user_info = current_user_info
        self.request_info = request_info
        self.request_params = request_params
        self.params = params
        self._transaction_id = str(uuid.uuid4())

    def __enter__(self):
        self.session = self.session_factory()
        self._start_transaction()
        return self

    def __exit__(self, type, value, traceback):
        if type is not None:
            try:
                self.rollback()
            except Exception:
                pass
            # SSL 断连等底层异常会让 session 进入不可用状态，
            # 必须从 scoped_session 注册表中移除，否则同线程下一个请求会拿到坏 session
            try:
                self.session_factory.remove()
            except Exception:
                pass
        else:
            self.commit()
        self._end_transaction(type is None)
        try:
            self.session.close()
        except Exception:
            pass

    def commit(self):
        self.session.commit()
        self._log_action(action=EnumTransactionLogAction.COMMITTED.value)

    def rollback(self):
        self.session.rollback()
        self._log_action(action=EnumTransactionLogAction.ROLLED_BACK.value)

    @contextmanager
    def start(self):
        if self.session is not None:
            raise RuntimeError("Session already started")
        self.session = self.session_factory()
        try:
            yield self.session
            self.commit()
        except Exception:
            self.rollback()
            raise
        finally:
            self.session.close()
            self.session = None

    def _add_record_to_database_table(
            self,
            model: T_BaseModel,
            entity: Type[U_BaseEntity]
    ):
        self._base_repository.add(
            model=model,
            entity=entity,
            commit_immediately=True
        )

    def _update_to_database_table_record(
            self,
            model: T_BaseModel,
            entity_id: str,
            entity: Type[U_BaseEntity]
    ):
        self._base_repository.update_entity(
            model=model,
            entity_id=entity_id,
            entity=entity,
        )

    def _start_transaction(self):
        """
        在 transaction 表中记录开始信息
        """
        if self.current_user_info is None or self.request_info is None:
            return

        transaction_model = TransactionModel(
            id=self._transaction_id,
            current_user_info=self.current_user_info,
            start_time=datetime.datetime.now(),
            end_time=None,
            status=EnumTransactionStatus.STARTED.value,
            request_info=self.request_info.model_dump(),
            request_params=self.request_params,
            params=self.params,
        )

        self._add_record_to_database_table(
            model=transaction_model,
            entity=TransactionEntity
        )

        self._log_action(action=EnumTransactionLogAction.STARTED.value)

    def _end_transaction(self, committed: bool):
        """
        更新 transaction 表中的结束信息
        """
        if self.current_user_info is None or self.request_info is None:
            return
        status = EnumTransactionStatus.COMMITTED.value if committed else EnumTransactionStatus.ROLLED_BACK.value
        model = self._base_repository.get_model_by_id(
            entity_id=self._transaction_id,
            entity=TransactionEntity
        )
        model.end_time = datetime.datetime.now()
        model.status = status
        self._update_to_database_table_record(
            model=model,
            entity_id=self._transaction_id,
            entity=TransactionEntity
        )
        self._log_action(action=EnumTransactionLogAction.ENDED.value)

    def _log_action(self, action: str, params: Dict = None):
        """
        在 log 表中记录操作信息
        """
        if self.current_user_info is None or self.request_info is None:
            return
        self._add_record_to_database_table(
            model=TransactionLogModel(
                transaction_id=self._transaction_id,
                action=action,
                params=params,
            ),
            entity=TransactionLogEntity
        )
