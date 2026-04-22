from datetime import datetime
from typing import Optional, List

from pydantic import Field

from basic.model.basic_model import BasicVersionModel, BasisModel


class InviteCodeModel(BasicVersionModel):
    code: Optional[str] = Field(None, description="邀请码")
    brief: Optional[str] = Field(None, description="邀请码简介")
    max_limit: Optional[int] = Field(None, description="最大使用次数")
    register_num: Optional[int] = Field(None, description="已使用次数")
    deadline: Optional[datetime] = Field(None, description="截止时间")
    enabled: bool = Field(..., description="启用状态")
    deleted: bool = Field(..., description="删除状态")


class InviteCodePageParamsModel(BasisModel):
    page_index: int = Field(1, description="分页索引")
    page_size: int = Field(20, description="分页大小")
    search: Optional[str] = Field(None, description="搜索关键词")
    search_fields: Optional[List[str]] = Field(None, description="搜索字段列表")


class EditInviteCodeParamsModel(InviteCodeModel):
    enabled: Optional[bool] = Field(True, description="启用")
    deleted: Optional[bool] = Field(False, description="删除")

    def to_invite_code_model(self) -> InviteCodeModel:
        return InviteCodeModel(
            id=self.id,
            code=self.code,
            brief=self.brief,
            max_limit=self.max_limit,
            deadline=self.deadline,
            enabled=self.enabled,
            deleted=self.deleted
        )


class SoftDeleteInviteCodeParamsModel(BasisModel):
    invite_code_id: str = Field(..., description="邀请码ID")


class ChangeInviteCodeEnableParamsModel(BasisModel):
    invite_code_id: str = Field(..., description="邀请码ID")
    enabled: Optional[bool] = Field(False, description="Enabled Status")


class InviteCodeStatisticsModel(BasisModel):
    total: int = Field(0, description="总数")
    run_out: int = Field(0, description="已用完")
    not_run_out: int = Field(0, description="未用完")
    expired: int = Field(0, description="已过期")
