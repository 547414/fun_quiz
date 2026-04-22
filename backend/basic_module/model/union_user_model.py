from typing import Optional, List, Dict

from pydantic import Field

from basic.model.basic_model import BasicVersionModel, BasisModel, BasicModel


class UnionUserUserRoleDetailItemModel(BasisModel):
    role_name: Optional[str] = Field(None, description="角色名称")
    role_code: Optional[str] = Field(None, description="角色编码")


class UnionUserUserOrganizationDetailItemModel(BasicModel):
    name: Optional[str] = Field(None, description="名称")
    name_list: Optional[List[str]] = Field(None, description="名称列表（路径）")


class UnionUserUserDeptDetailItemModel(BasicModel):
    name: Optional[str] = Field(None, description="名称")
    name_list: Optional[List[str]] = Field(None, description="名称列表（路径）")


class UnionUserUserInfoDetailModel(BasisModel):
    name: Optional[str] = Field(None, description="用户名称")
    role_list: Optional[List[UnionUserUserRoleDetailItemModel]] = Field(None, description="角色列表")


class UnionUserUserInfoModel(BasisModel):
    role_data: Optional[Dict[str, UnionUserUserInfoDetailModel]] = Field(None, description="角色数据")


class UnionUserModel(BasicVersionModel):
    name: Optional[str] = Field(None, description="名称")
    enabled: Optional[bool] = Field(True, description="是否启用")
    is_deleted: Optional[bool] = Field(False, description="是否已删除")


class UnionUserInfoListModel(BasicVersionModel):
    union_user_user_category: Optional[str] = Field(None, description="用户类别")
    union_user_user_id: Optional[str] = Field(None, description="用户ID")
    union_user_user_name: Optional[str] = Field(None, description="用户名称")
    current_role_code: Optional[str] = Field(None, description="当前角色编码")
    union_user_user_role_list: Optional[List[UnionUserUserRoleDetailItemModel]] = Field(
        None,
        description="用户角色列表"
    )
    organization_list: Optional[List[UnionUserUserOrganizationDetailItemModel]] = Field(None, description="组织列表")
    dept_list: Optional[List[UnionUserUserDeptDetailItemModel]] = Field(None, description="部门列表")


class UnionUserInfoModel(BasicVersionModel):
    name: Optional[str] = Field(None, description="名称")
    user_list: Optional[List[UnionUserInfoListModel]] = Field(None, description="用户列表")
    user_id_list: Optional[List[str]] = Field(None, description="用户ID列表")
    union_user_user_info: Optional[UnionUserUserInfoModel] = Field(None, description="角色数据")


class EditUnionUserInfoModel(BasisModel):
    union_user_id: Optional[str] = Field(None, description="用户ID")
    name: Optional[str] = Field(None, description="名称")


class UnionUserPageParamsModel(BasisModel):
    page_index: int = Field(1, description="页码")
    page_size: int = Field(20, description="分页大小")
    search: Optional[str] = Field(None, description="搜索关键字")
    search_fields: Optional[List[str]] = Field(None, description="搜索字段")


class UnionUserAuthCodeLoginParamsModel(BasisModel):
    auth_code: str = Field(1, description="授权码")


class RefreshUnionUserAccessTokenModel(BasisModel):
    refresh_token: str = Field(..., description="刷新令牌")


class UnionUserLoginResultModel(BasisModel):
    access_token: str = Field(..., description="访问令牌")
    refresh_token: str = Field(..., description="刷新令牌")
    token_type: str = Field(..., description="令牌类型")
    union_user_info: Optional[UnionUserInfoModel] = Field(None, description="联合用户信息")
    scene: Optional[str] = Field(None, description="场景")
    space: Optional[str] = Field(None, description="空间")


class RefreshUnionUserAccessTokenViewModel(BasisModel):
    token_type: str = Field(..., description="令牌类型")
    access_token: str = Field(..., description="访问令牌")


class DeleteUnionUserModel(BasisModel):
    union_user_id: str = Field(..., description="联合用户ID")
