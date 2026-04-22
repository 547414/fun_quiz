import secrets
import string
from datetime import datetime, timedelta, timezone

from basic.error.base_error import BusinessError
from basic_module.model.invite_code_model import InviteCodePageParamsModel, EditInviteCodeParamsModel, \
    SoftDeleteInviteCodeParamsModel, ChangeInviteCodeEnableParamsModel
from basic_module.model.validate_token_model import ValidateTokenResModel
from basic_module.repository.invite_code_repository import InviteCodeRepository


class InviteCodeService:
    def __init__(
            self,
            invite_code_repository: InviteCodeRepository,
    ):
        self.__invite_code_repository = invite_code_repository

    def get_invite_code_page(
            self,
            params: InviteCodePageParamsModel
    ):
        return self.__invite_code_repository.get_company_page(
            params=params
        )

    def edit(
            self,
            params: EditInviteCodeParamsModel,
            current_user_info: ValidateTokenResModel
    ):
        if params.id:
            exist = self.__invite_code_repository.get_by_id(
                invite_code_id=params.id
            )
            if not exist:
                raise BusinessError('未找到邀请码')
            exist.brief = params.brief
            exist.max_limit = params.max_limit
            exist.deadline = params.deadline
            exist.enabled = params.enabled
            self.__invite_code_repository.update(
                model=exist
            )
        else:
            params.code = self.generate_secure_key()
            self.__invite_code_repository.insert(
                model=params.to_invite_code_model()
            )

    @staticmethod
    def generate_secure_key(length=32):
        charset = string.ascii_letters + string.digits
        while True:
            key = ''.join(secrets.choice(charset) for _ in range(length))
            if (any(c.islower() for c in key) and
                    any(c.isupper() for c in key) and
                    any(c.isdigit() for c in key)):
                return key

    def soft_delete(
            self,
            params: SoftDeleteInviteCodeParamsModel,
            current_user_info: ValidateTokenResModel
    ):
        exist = self.__invite_code_repository.get_by_id(
            invite_code_id=params.invite_code_id
        )
        if not exist:
            raise BusinessError('未找到邀请码')
        exist.deleted = True
        self.__invite_code_repository.update(
            model=exist
        )

    def get_invite_code_detail(self, invite_code_id: str):
        exist = self.__invite_code_repository.get_by_id(
            invite_code_id=invite_code_id
        )
        if not exist:
            raise BusinessError('未找到邀请码')
        return exist

    def change_enabled(
            self,
            params: ChangeInviteCodeEnableParamsModel,
            current_user_info: ValidateTokenResModel
    ):
        exist = self.__invite_code_repository.get_by_id(
            invite_code_id=params.invite_code_id
        )
        if not exist:
            raise BusinessError('未找到公司')
        exist.enabled = params.enabled
        self.__invite_code_repository.update(
            model=exist
        )

    def check_invite_code(
            self,
            invite_code: str,
    ):
        exist = self.__invite_code_repository.get_by_code(
            code=invite_code
        )
        if not exist:
            raise BusinessError('邀请码不存在')
        if exist.deleted:
            raise BusinessError('邀请码已失效')
        if not exist.enabled:
            raise BusinessError('邀请码已失效')
        if exist.max_limit <= exist.register_num:
            raise BusinessError('邀请码已失效（已达注册上限）')
        utc8 = timezone(timedelta(hours=8))
        if exist.deadline < datetime.now(utc8):
            raise BusinessError('邀请码已失效')

    def update_register_num(
            self,
            invite_code: str,
    ):
        exist = self.__invite_code_repository.get_by_code(
            code=invite_code
        )
        exist.register_num += 1
        self.__invite_code_repository.update(
            model=exist
        )

    def statistics(self):
        return self.__invite_code_repository.statistics()
