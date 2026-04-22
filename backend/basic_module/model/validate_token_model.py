from typing import Optional
from pydantic import Field
from basic.model.basic_model import BasisModel
from basic_module.model.union_user_model import UnionUserInfoModel, UnionUserInfoListModel


class ValidateTokenResModel(BasisModel):
    current_role_code: Optional[str] = Field(None, description="当前角色编码")
    union_user_info: Optional[UnionUserInfoModel] = Field(None, description="联合用户信息")
    current_user: Optional[UnionUserInfoListModel] = Field(None, description="当前请求后端接口的用户信息")
