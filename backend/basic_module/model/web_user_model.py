from typing import Optional, List

from pydantic import Field

from basic.model.basic_model import BasicVersionModel, BasisModel, BasicModel
from basic.model.page_sort_model import EnumPageSortModel
from basic_module.model.role_model import EnumRoleCode
from basic_module.model.union_user_model import UnionUserInfoModel
from basic_module.model.upload_model import UploadResModel


class WebUserModel(BasicVersionModel):
    name: str = Field(..., description='用户名')
    mobile: Optional[str] = Field(None, description='手机号')
    email: Optional[str] = Field(None, description='邮箱')
    enabled: bool = Field(True, description='是否启用')
    avatar_file_info: Optional[UploadResModel] = Field(None, description='头像文件信息')
    password_salt: str = Field(..., description='密码盐')
    password_hash: str = Field(..., description='密码哈希')
    try_count: int = Field(0, description='尝试次数')
    reset_password: bool = Field(False, description='是否重置密码')


class WebUserLoginParamsModel(BasisModel):
    name: Optional[str] = Field(None, description='用户名')
    password: Optional[str] = Field(None, description='密码')
    verification_code: Optional[str] = Field(None, description='验证码')
    scene_id: Optional[str] = Field(None, description='场景ID')
    union_user_id: Optional[str] = Field(None, description='联合用户ID')
    captcha_id: Optional[str] = Field(None, description='验证码ID')
    validate_captcha_auth_code: Optional[str] = Field(None, description='验证码校验码')


class WebOauthLoginParamsModel(BasisModel):
    auth_code: str = Field(..., description='授权码')
    wecom_user_uuid: str = Field(..., description='企微用户UUID')


class WebUserInfoRoleModel(BasisModel):
    role_name: str = Field(..., description='角色名称')
    role_code: EnumRoleCode = Field(..., description='角色编码')


class WebUserViewModel(BasicModel):
    name: str = Field(..., description='用户名')
    mobile: Optional[str] = Field(None, description='手机号')
    email: Optional[str] = Field(None, description='邮箱')
    avatar_file_info: Optional[UploadResModel] = Field(None, description='头像文件ID')
    role_list: List[WebUserInfoRoleModel] = Field(..., description='角色列表')
    role_name: str = Field(..., description='角色名称')
    role_code: EnumRoleCode = Field(..., description='角色编码')
    reset_password: bool = Field(False, description='是否重置密码')
    wecom_user_uuid: Optional[str] = Field(None, description='企微用户UUID')
    union_user_info: Optional[UnionUserInfoModel] = Field(None, description='联合用户信息')


class UserOrganizationDetailItemModel(BasicModel):
    name: Optional[str] = Field(None, description="名称")
    name_list: Optional[List[str]] = Field(None, description="名称列表（路径）")


class UserDeptDetailItemModel(BasicModel):
    name: Optional[str] = Field(None, description="名称")
    name_list: Optional[List[str]] = Field(None, description="名称列表（路径）")


class AddWebUserModel(BasisModel):
    name: str = Field(..., description='用户名')
    role_code_list: List[str] = Field(..., description='角色编码列表')
    avatar_file_info: Optional[UploadResModel] = Field(None, description='头像文件ID')
    password: str = Field(..., description='密码')
    password_repeat: str = Field(..., description='重复密码')
    mobile: Optional[str] = Field(None, description='手机号')
    email: Optional[str] = Field(None, description='邮箱')
    wecom_user_uuid: Optional[str] = Field(None, description='企微用户UUID')
    union_user_uuid: Optional[str] = Field(None, description='联合用户UUID')
    wx_user_id: Optional[str] = Field(None, description='微信用户ID')
    enabled: bool = Field(True, description='是否启用')
    organization_list: Optional[List[UserOrganizationDetailItemModel]] = Field(None, description="组织列表")
    dept_list: Optional[List[UserDeptDetailItemModel]] = Field(None, description="部门列表")


class EditWebUserModel(BasicModel):
    name: str = Field(..., description='用户名')
    role_code_list: List[str] = Field(..., description='角色编码列表')
    avatar_file_info: Optional[UploadResModel] = Field(None, description='头像文件ID')
    mobile: Optional[str] = Field(None, description='手机号')
    email: Optional[str] = Field(None, description='邮箱')
    wecom_user_uuid: Optional[str] = Field(None, description='企微用户UUID')
    wx_user_id: Optional[str] = Field(None, description='微信用户ID')
    union_user_uuid: Optional[str] = Field(None, description='联合用户UUID')
    enabled: bool = Field(True, description='是否启用')
    organization_list: Optional[List[UserOrganizationDetailItemModel]] = Field(None, description="组织列表")
    dept_list: Optional[List[UserDeptDetailItemModel]] = Field(None, description="部门列表")


class WebUserDetailModel(BasicModel):
    name: str = Field(..., description='用户名')
    role_list: List[WebUserInfoRoleModel] = Field(..., description='角色列表')
    avatar_file_info: Optional[UploadResModel] = Field(None, description='头像文件ID')
    mobile: Optional[str] = Field(None, description='手机号')
    email: Optional[str] = Field(None, description='邮箱')
    wecom_user_uuid: Optional[str] = Field(None, description='企微用户UUID')
    wx_user_id: Optional[str] = Field(None, description='微信用户ID')
    wecom_user_name: Optional[str] = Field(None, description='企微用户名')
    union_user_uuid: Optional[str] = Field(None, description='联合用户UUID')
    union_user_name: Optional[str] = Field(None, description='联合用户名')
    enabled: bool = Field(True, description='是否启用')
    organization_list: Optional[List[UserOrganizationDetailItemModel]] = Field(None, description="组织列表")
    dept_list: Optional[List[UserDeptDetailItemModel]] = Field(None, description="部门列表")


class WebUserPageOrganizationModel(BasicModel):
    name: str = Field(..., description='，名称')
    name_list: List[str] = Field(..., description='名称列表（路径）')


class WebUserPageDeptModel(BasicModel):
    name: str = Field(..., description='，名称')
    name_list: List[str] = Field(..., description='名称列表（路径）')


class WebUserPageViewModel(BasicModel):
    name: str = Field(..., description='用户名')
    mobile: Optional[str] = Field(None, description='手机号')
    email: Optional[str] = Field(None, description='邮箱')
    enabled: bool = Field(True, description='是否启用')
    avatar_file_info: Optional[UploadResModel] = Field(None, description='头像文件ID')
    role_list: List[WebUserInfoRoleModel] = Field(..., description='角色列表')
    wecom_user_uuid: Optional[str] = Field(None, description='企微用户UUID')
    wecom_user_name: Optional[str] = Field(None, description='企微用户名')
    union_user_uuid: Optional[str] = Field(None, description='联合用户UUID')
    union_user_name: Optional[str] = Field(None, description='联合用户名')
    organization_list: Optional[List[WebUserPageOrganizationModel]] = Field(None, description='组织列表')
    dept_list: Optional[List[WebUserPageDeptModel]] = Field(None, description='部门列表')


class ResetWebUserPasswordModel(BasisModel):
    user_id: str = Field(..., description='用户ID')


class ResetWebUserSelfPasswordModel(BasisModel):
    old_password: str = Field(..., description='旧密码')
    new_password: str = Field(..., description='新密码')
    new_password_repeat: str = Field(..., description='重复新密码')


class UserRegisterParamsModel(BasisModel):
    captcha_id: str = Field(..., description="验证码ID")
    validate_auth_code: str = Field(..., description="验证码校验码")
    name: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")
    invite_code: Optional[str] = Field(None, description="邀请码")


class UserPageParamsModel(BasisModel):
    page_index: int = Field(1, description="页码")
    page_size: int = Field(20, description="分页大小")
    search: Optional[str] = Field(None, description="搜索关键字")
    search_fields: Optional[List[str]] = Field(None, description="搜索字段")
    name_sort: Optional[EnumPageSortModel] = Field(None, description="名称排序")
    role_code_list: Optional[List[str]] = Field(None, description="角色编码列表")


class ChangeUserEnabledParamsModel(BasicModel):
    enabled: bool = Field(..., description="启用")


class ChangeCurrentUserRoleParamsModel(BasicModel):
    role_code: str = Field(..., description="角色编码")


class UserListParamsModel(BasisModel):
    user_id_list: List[str] = Field(..., description="用户ID列表")
