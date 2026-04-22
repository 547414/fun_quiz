import hashlib
import os
import secrets
import uuid
from datetime import timedelta, datetime, timezone
from typing import Dict, List

import jwt
import toml
from fastapi import HTTPException
from openai import organization

from basic.api_response.api_response import ApiResponse
from basic.error.base_error import BusinessError
from basic.minio_client.minio_client import MinioClient
from basic.redis_client.redis_client import RedisClient
from basic_module.model.auth_model import JwtPayloadInfo, EnumUserCategory
from basic_module.model.role_model import EnumRoleCode
from basic_module.model.union_user_model import UnionUserInfoModel, UnionUserModel, UnionUserLoginResultModel
from basic_module.model.union_user_user_model import UnionUserUserModel, EnumUnionUserCategory
from basic_module.model.upload_model import UploadResModel
from basic_module.model.web_user_dept_model import WebUserDeptModel
from basic_module.model.web_user_model import WebUserLoginParamsModel, \
    WebUserModel, AddWebUserModel, EditWebUserModel, ResetWebUserPasswordModel, ResetWebUserSelfPasswordModel, \
    WebOauthLoginParamsModel, UserRegisterParamsModel, ChangeCurrentUserRoleParamsModel, UserPageParamsModel, \
    ChangeUserEnabledParamsModel, UserListParamsModel
from basic_module.model.user_role_model import EnumUserRoleCategory, UserRoleModel
from basic_module.model.validate_token_model import ValidateTokenResModel
from basic_module.model.web_user_organization_model import WebUserOrganizationModel
from basic_module.repository.backend_api_repository import BackendApiRepository
from basic_module.repository.dept_repository import DeptRepository
from basic_module.repository.organization_repository import OrganizationRepository
from basic_module.repository.role_repository import RoleRepository
from basic_module.repository.union_user_repository import UnionUserRepository
from basic_module.repository.union_user_user_repository import UnionUserUserRepository
from basic_module.repository.web_user_dept_repository import WebUserDeptRepository
from basic_module.repository.web_user_organization_repository import WebUserOrganizationRepository
from basic_module.repository.web_user_repository import WebUserRepository
from basic_module.repository.user_role_repository import UserRoleRepository
from basic_module.service.invite_code_service import InviteCodeService
from basic_module.service.tools_service import ToolsService
from basic_module.service.union_user_user_service import UnionUserUserService
from basic_module.service.user_role_service import UserRoleService
from basic_module.service.web_user_dept_service import WebUserDeptService
from basic_module.service.web_user_organization_service import WebUserOrganizationService


class WebUserService:
    def __init__(
            self,
            web_user_repository: WebUserRepository,
            user_role_service: UserRoleService,
            backend_api_repository: BackendApiRepository,
            redis_client: RedisClient,
            minio_client: MinioClient,
            union_user_user_service: UnionUserUserService,
            union_user_repository: UnionUserRepository,
            union_user_user_repository: UnionUserUserRepository,
            role_repository: RoleRepository,
            user_role_repository: UserRoleRepository,
            organization_repository: OrganizationRepository,
            web_user_organization_repository: WebUserOrganizationRepository,
            dept_repository: DeptRepository,
            web_user_dept_repository: WebUserDeptRepository,
            invite_code_service: InviteCodeService,
            tools_service: ToolsService,
            web_user_organization_service: WebUserOrganizationService,
            web_user_dept_service: WebUserDeptService,
    ):
        self.__web_user_repository = web_user_repository
        self.__user_role_service = user_role_service
        self.__backend_api_repository = backend_api_repository
        self.__redis_client = redis_client
        self.__minio_client = minio_client
        self.__union_user_user_service = union_user_user_service
        self.__union_user_repository = union_user_repository
        self.__union_user_user_repository = union_user_user_repository
        self.__role_repository = role_repository
        self.__user_role_repository = user_role_repository
        self.__organization_repository = organization_repository
        self.__web_user_organization_repository = web_user_organization_repository
        self.__dept_repository = dept_repository
        self.__web_user_dept_repository = web_user_dept_repository
        self.__invite_code_service = invite_code_service
        self.__tools_service = tools_service
        self.__web_user_organization_service = web_user_organization_service
        self.__web_user_dept_service = web_user_dept_service

        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.__base_path = os.path.join(path, "../")
        self.__app_config = toml.load(fr"{self.__base_path}/app_config.toml")
        self.__active = self.__app_config.get('settings', {}).get('active', 'development')
        self.__config_name = f'app_{self.__active}_config.toml'
        self.__config = toml.load(fr"{self.__base_path}/config/{self.__config_name}")
        self.__expired_detail = ApiResponse(code=40111, message="令牌已过期").to_json()
        self.__refresh_expired_detail = ApiResponse(code=40112, message="刷新令牌已过期").to_json()
        self.__invalid_detail = ApiResponse(code=40121, message="令牌无效").to_json()
        self.__refresh_invalid_detail = ApiResponse(code=40122, message="刷新令牌无效").to_json()
        self.__missing_detail = ApiResponse(code=40131, message="令牌缺失").to_json()
        self.__refresh_missing_detail = ApiResponse(code=40132, message="刷新令牌缺失").to_json()
        self.__revoked_detail = ApiResponse(code=40141, message="令牌已禁用").to_json()
        self.__refresh_revoked_detail = ApiResponse(code=40142, message="刷新令牌已禁用").to_json()
        self.__no_permission_detail = ApiResponse(code=40151, message="没有权限").to_json()

    def user_login(self, params: WebUserLoginParamsModel, scene: str = "DEFAULT", space: str = "DEFAULT"):
        if not params.validate_captcha_auth_code or not params.captcha_id:
            raise BusinessError("请先进行安全验证")
        validate_auth_code_redis = self.__redis_client.get_value(
            key=f"captcha_validate_auth_code_{params.captcha_id}"
        )
        if validate_auth_code_redis != params.validate_captcha_auth_code:
            raise BusinessError(code=50001, message='安全验证失效，请重新进行验证')

        if params.scene_id:
            redis_info = self.__redis_client.get_value(
                f"qr_code_scene_{params.scene_id}"
            )
            if not redis_info:
                return None
            user = self.__web_user_repository.get_user_by_union_user_id(
                union_user_id=redis_info
            )
        else:
            user = self.__web_user_repository.get_by_name(params.name)

        if not user:
            raise BusinessError("用户不存在")

        if user.enabled is False:
            raise BusinessError("用户已被禁用")

        if not params.scene_id:
            sha256_hash = hashlib.sha256()
            sha256_hash.update((params.password + user.password_salt).encode('utf-8'))
            hash_value = sha256_hash.hexdigest()
            if hash_value != user.password_hash:
                self.update_try_count(user=user)

        # verification_code = self.__redis_client.get_value(f"verification_code:{params.name}")
        # if verification_code != params.verification_code:
        #     raise BusinessError("Invalid verification code")

        user.try_count = 0
        self.__web_user_repository.update(model=user)

        jwt_payload = JwtPayloadInfo(
            union_user_info=self.get_union_user_info(user_id=user.id),
        )
        return self.generate_user_token(
            jwt_payload=jwt_payload,
            scene=scene,
            space=space
        )

    def get_union_user_info(self, user_id: str, current_role_code: str = None):
        union_user = self.__web_user_repository.get_union_user_by_user_id(
            user_id=user_id
        )
        union_user_user_info = self.__union_user_repository.get_user_info(
            user_id_list=union_user.user_id_list
        )
        union_user.union_user_user_info = union_user_user_info
        for user in union_user.user_list:
            role_data = union_user_user_info.role_data
            data_key = user.union_user_user_id.replace('-', '_')
            if role_data.get(data_key):
                user.union_user_user_name = role_data.get(data_key).name
                user.union_user_user_role_list = role_data.get(data_key).role_list
                if len(user.union_user_user_role_list) > 0:
                    if current_role_code:
                        user.current_role_code = current_role_code
                        break
                    else:
                        user.current_role_code = user.union_user_user_role_list[0].role_code
                        break
        return union_user

    def web_oauth_login(self, params: WebOauthLoginParamsModel):
        # 判断auth_code是否有效
        if not self.__redis_client.exists(params.auth_code):
            raise Exception("授权码无效")
        self.__redis_client.delete_key(params.auth_code)

        user = self.__web_user_repository.get_user_by_wecom_user_uuid(
            wecom_user_uuid=params.wecom_user_uuid
        )
        if not user:
            raise BusinessError("用户不存在")

        user_info = self.__web_user_repository.get_info(user_id=user.id)
        if user.enabled is False:
            raise BusinessError("用户已被禁用")

        union_user = self.__web_user_repository.get_union_user_by_user_id(
            user_id=user.id
        )
        jwt_payload = JwtPayloadInfo(
            union_user_info=union_user,
        )
        user_info.union_user_info = union_user
        return self.generate_user_token(
            jwt_payload=jwt_payload,
        )

    def generate_user_token(
            self,
            jwt_payload: JwtPayloadInfo,
            scene: str = "DEFAULT",
            space: str = "DEFAULT",
    ):
        access_token = self.__create_access_token(data=jwt_payload)
        refresh_token = self.__create_refresh_token(data=jwt_payload)

        # 将 Access Token 和 Refresh Token 存入 Redis
        self.__redis_client.set_value(
            f"access_token_{space}:{jwt_payload.union_user_info.id}_{scene}",
            access_token,
            expiration=int(timedelta(minutes=self.__config['jwt']['ACCESS_TOKEN_EXPIRE_MINUTES']).total_seconds())
        )
        self.__redis_client.set_value(
            f"refresh_token_{space}:{jwt_payload.union_user_info.id}_{scene}",
            refresh_token,
            expiration=timedelta(days=self.__config['jwt']['REFRESH_TOKEN_EXPIRE_DAYS']).seconds
        )

        for user in jwt_payload.union_user_info.user_list:
            if user.current_role_code:
                self.__redis_client.set_value(
                    f"current_user_role_{user.union_user_user_category}:{jwt_payload.union_user_info.id}",
                    user.current_role_code,
                    expiration=timedelta(days=self.__config['jwt']['REFRESH_TOKEN_EXPIRE_DAYS']).seconds
                )

        return UnionUserLoginResultModel(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=self.__config['jwt']['TOKEN_TYPE'],
            union_user_info=jwt_payload.union_user_info,
            scene=scene,
            space=space
        )

    def refresh_user_token(
            self,
            jwt_payload: JwtPayloadInfo,
            scene: str = "DEFAULT",
            space: str = "DEFAULT",
    ):
        access_token = self.__create_access_token(data=jwt_payload)
        refresh_token = self.__redis_client.get_value(
            key=f"refresh_token_{space}:{jwt_payload.union_user_info.id}_{scene}"
        )

        # 将 Access Token 和 Refresh Token 存入 Redis
        self.__redis_client.set_value(
            f"access_token_{space}:{jwt_payload.union_user_info.id}_{scene}",
            access_token,
            expiration=int(timedelta(minutes=self.__config['jwt']['ACCESS_TOKEN_EXPIRE_MINUTES']).total_seconds())
        )

        for user in jwt_payload.union_user_info.user_list:
            if user.current_role_code:
                self.__redis_client.set_value(
                    f"current_user_role_{space}:{jwt_payload.union_user_info.id}_{scene}",
                    user.current_role_code,
                    expiration=timedelta(days=self.__config['jwt']['REFRESH_TOKEN_EXPIRE_DAYS']).seconds
                )

        return UnionUserLoginResultModel(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=self.__config['jwt']['TOKEN_TYPE'],
            union_user_info=jwt_payload.union_user_info,
            scene=scene,
            space=space
        )

    def change_current_user_role(
            self,
            params: ChangeCurrentUserRoleParamsModel,
            current_user_info: ValidateTokenResModel,
            scene: str = "DEFAULT",
            space: str = "DEFAULT"
    ):
        user = self.__web_user_repository.get_user_by_union_user_id(
            union_user_id=current_user_info.union_user_info.id
        )
        if not user:
            raise BusinessError("用户不存在")
        user_info = self.__web_user_repository.get_info(user_id=user.id)
        no_role = True
        for role in user_info.role_list:
            if role.role_code.value == params.role_code:
                no_role = False
                user_info.role_name = role.role_name
                user_info.role_code = role.role_code
        if no_role:
            raise BusinessError("用户没有该角色")
        jwt_payload = JwtPayloadInfo(
            union_user_info=self.get_union_user_info(user_id=user.id, current_role_code=params.role_code),
        )
        return self.refresh_user_token(
            jwt_payload=jwt_payload,
            scene=scene,
            space=space
        )

    def update_try_count(
            self,
            user: WebUserModel,
    ):
        user.try_count += 1
        if user.try_count < 5:
            self.__web_user_repository.update(model=user)
            raise BusinessError(f"用户名或密码错误，还有{5 - user.try_count}次机会")
        else:
            now = datetime.utcnow().replace(tzinfo=timezone.utc)
            if now - user.updated_at > timedelta(days=1):
                user.try_count = 0
                self.__web_user_repository.update(model=user)
                raise BusinessError("用户名或密码错误，还有4次机会")
            else:
                raise BusinessError("尝试次数过多，请明天再试")

    def user_logout(
            self,
            user_id: str,
            user_category: str = 'WEB_USER'
    ):
        access_token = self.__redis_client.get_value(f"access_token_{user_category}:{user_id}")
        refresh_token = self.__redis_client.get_value(f"refresh_token_{user_category}:{user_id}")

        if access_token:
            self.revoke_token(access_token, "access")
        if refresh_token:
            self.revoke_token(refresh_token, "refresh")

        # 移除存储的 tokens
        self.__redis_client.delete_key(f"access_token_{user_category}:{user_id}")
        self.__redis_client.delete_key(f"refresh_token_{user_category}:{user_id}")

    def revoke_token(self, token: str, token_type: str):
        """将 Token 放入黑名单"""
        expiration_time = jwt.decode(
            token, self.__config['jwt']['SECRET_KEY'], algorithms=[self.__config['jwt']['ALGORITHM']]
        )['exp']

        remaining_time = expiration_time - datetime.utcnow().timestamp()
        self.__redis_client.set_value(
            f"blacklist:{token_type}_token:{token}",
            "revoked",
            expiration=int(remaining_time)
        )

    def is_token_revoked(self, token: str, token_type: str) -> bool:
        """检查 Token 是否在黑名单中"""
        return self.__redis_client.get_value(f"blacklist:{token_type}_token:{token}") is not None

    def __create_access_token(self, data: JwtPayloadInfo) -> str:
        """生成短期有效的 Access Token"""
        data.convert_names = False
        to_encode = data.model_dump().copy()
        expire = datetime.utcnow() + timedelta(minutes=self.__config['jwt']['ACCESS_TOKEN_EXPIRE_MINUTES'])
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            self.__config['jwt']['SECRET_KEY'],
            algorithm=self.__config['jwt']['ALGORITHM']
        )
        return encoded_jwt

    def __create_refresh_token(self, data: JwtPayloadInfo) -> str:
        """生成长期有效的 Refresh Token"""
        data.convert_names = False
        to_encode = data.model_dump().copy()
        expire = datetime.utcnow() + timedelta(days=self.__config['jwt']['REFRESH_TOKEN_EXPIRE_DAYS'])
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            self.__config['jwt']['SECRET_KEY'],
            algorithm=self.__config['jwt']['ALGORITHM']
        )
        return encoded_jwt

    def check_backend_api_permission(
            self,
            url: str,
            current_user_info: ValidateTokenResModel,
    ):
        allow_backend_api = self.__backend_api_repository.get_allow_backend_api(
            url=url,
            role_code=current_user_info.current_role_code
        )
        if not allow_backend_api:
            raise HTTPException(status_code=403, detail=self.__no_permission_detail)

    def check_backend_api_ignore(
            self,
            url: str,
    ):
        backend_api = self.__backend_api_repository.get_by_url(
            url=url
        )
        if not backend_api:
            raise HTTPException(status_code=403, detail=self.__no_permission_detail)
        return backend_api.ignore_auth

    def add_user(self, params: AddWebUserModel):
        self.check_add_user_data(params=params)
        salt = secrets.token_hex(16)
        sha256_hash = hashlib.sha256()
        sha256_hash.update((params.password + salt).encode('utf-8'))
        hash_value = sha256_hash.hexdigest()

        params.avatar_file_info.url = None
        user_id = str(uuid.uuid4())
        user = WebUserModel(
            id=user_id,
            name=params.name,
            mobile=params.mobile,
            email=params.email,
            enabled=params.enabled,
            avatar_file_info=params.avatar_file_info,
            password_salt=salt,
            password_hash=hash_value,
            try_count=0
        )
        self.__web_user_repository.insert(model=user)

        self.__user_role_service.add_user_role(
            user_id=user.id, role_code_list=params.role_code_list
        )

        union_user_id = str(uuid.uuid4())
        self.__union_user_repository.insert(
            model=UnionUserModel(
                id=union_user_id,
                name=params.name,
            )
        )
        params.union_user_uuid = union_user_id
        self.__union_user_user_service.edit_web_user_relation(
            user_id=user.id,
            union_user_uuid=params.union_user_uuid
        )
        if params.wx_user_id:
            self.__union_user_user_service.edit_web_user_relation(
                user_id=params.wx_user_id,
                union_user_uuid=params.union_user_uuid
            )
        if params.organization_list:
            self.sava_web_user_organization_by_organization(
                web_user_id=user_id,
                organization_id_list=[x.id for x in params.organization_list]
            )
        if params.dept_list:
            self.sava_web_user_dept_by_dept(
                web_user_id=user_id,
                dept_id_list=[x.id for x in params.dept_list]
            )

    def edit_user(self, params: EditWebUserModel, current_user_info: ValidateTokenResModel):
        user = self.__web_user_repository.get_by_id(user_id=params.id)
        if not user:
            raise BusinessError("用户不存在")
        exist_user = self.__web_user_repository.get_exist_by_name(
            user_id=params.id,
            user_name=params.name
        )
        if exist_user:
            raise BusinessError("用户名已存在")
        user_info = self.__web_user_repository.get_info(user_id=user.id)
        role_code_list = [role.role_code.value for role in user_info.role_list]
        if EnumRoleCode.SUPER_ADMIN.value in role_code_list:
            if current_user_info.current_role_code != EnumRoleCode.SUPER_ADMIN.value:
                raise BusinessError("没有权限")
        user.name = params.name
        user.mobile = params.mobile
        user.email = params.email
        if current_user_info.current_user.union_user_user_id != params.id:
            user.enabled = params.enabled
        user.avatar_file_info = params.avatar_file_info
        user.avatar_file_info.url = None
        self.__web_user_repository.update(model=user)

        if current_user_info.current_user.union_user_user_id != params.id:
            self.__user_role_service.edit_user_role(
                user_id=user.id, role_code_list=params.role_code_list
            )

        exist_union_user = self.__union_user_repository.get_by_web_user_id(
           web_user_id=params.id
        )
        if exist_union_user:
            union_user_id = exist_union_user.id
            exist_union_user.name = params.name
            exist_union_user.enabled = params.enabled
            self.__union_user_repository.update(
                model=exist_union_user
            )
        else:
            union_user_id = str(uuid.uuid4())
            self.__union_user_repository.insert(
                model=UnionUserModel(
                    id=union_user_id,
                    name=params.name,
                    enabled=True,
                    is_deleted=False,
                )
            )

        self.__union_user_user_service.edit_web_user_relation(
            user_id=user.id,
            union_user_uuid=union_user_id
        )
        if params.wx_user_id:
            self.__union_user_user_service.edit_web_user_relation(
                user_id=params.wx_user_id,
                union_user_uuid=params.union_user_uuid
            )
        if params.organization_list:
            self.sava_web_user_organization_by_organization(
                web_user_id=user.id,
                organization_id_list=[x.id for x in params.organization_list]
            )
        if params.dept_list:
            self.sava_web_user_dept_by_dept(
                web_user_id=user.id,
                dept_id_list=[x.id for x in params.dept_list]
            )

    def sava_web_user_organization_by_organization(
            self,
            web_user_id: str,
            organization_id_list: List[str],
    ):
        exist_list = self.__web_user_organization_repository.get_list_by_web_user_id(
            web_user_id=web_user_id
        )
        if not exist_list:
            exist_list = []
        for exist in exist_list:
            if exist.organization_id not in organization_id_list:
                self.__web_user_dept_repository.delete_by_id(
                    data_id=exist.id,
                )
        exist_organization_id_list = [x.organization_id for x in exist_list]
        for organization_id in organization_id_list:
            if organization_id not in exist_organization_id_list:
                self.__web_user_organization_repository.insert(
                    model=WebUserOrganizationModel(
                        web_user_id=web_user_id,
                        organization_id=organization_id,
                    )
                )

    def sava_web_user_dept_by_dept(
            self,
            web_user_id: str,
            dept_id_list: List[str],
    ):
        exist_list = self.__web_user_dept_repository.get_list_by_web_user_id(
            web_user_id=web_user_id
        )
        if not exist_list:
            exist_list = []
        for exist in exist_list:
            if exist.dept_id not in dept_id_list:
                self.__web_user_dept_repository.delete_by_id(
                    data_id=exist.id,
                )
        exist_dept_id_list = [x.dept_id for x in exist_list]
        for dept_id in dept_id_list:
            if dept_id not in exist_dept_id_list:
                self.__web_user_dept_repository.insert(
                    model=WebUserDeptModel(
                        web_user_id=web_user_id,
                        dept_id=dept_id,
                    )
                )

    def check_add_user_data(self, params: AddWebUserModel):
        user = self.__web_user_repository.get_by_name(params.name)
        if user:
            raise BusinessError("用户名已存在")
        if params.password != params.password_repeat:
            raise BusinessError("两次输入密码不一致")
        # 密码必须包含数字、大小写字母，6-20位
        if not any(map(str.isdigit, params.password)):
            raise BusinessError("密码必须包含数字")
        if not any(map(str.islower, params.password)):
            raise BusinessError("密码必须包含小写字母")
        if not any(map(str.isupper, params.password)):
            raise BusinessError("密码必须包含大写字母")
        if not 6 <= len(params.password) <= 20:
            raise BusinessError("密码长度必须在6-20位之间")

    def get_user_page(
            self,
            params: UserPageParamsModel,
            current_user_info: ValidateTokenResModel
    ):
        page = self.__web_user_repository.get_user_page(
            params=params,
            current_user_info=current_user_info
        )
        for data in page.data:
            if data.avatar_file_info:
                bucket_name = data.avatar_file_info.bucket_name
                object_name = data.avatar_file_info.object_name
                if not bucket_name or not object_name:
                    continue
                data.avatar_file_info.url = self.__minio_client.get_file_url(
                    bucket_name=bucket_name,
                    object_name=object_name
                )
        return page

    def get_by_id_list(self, params: UserListParamsModel):
        return self.__web_user_repository.get_by_id_list(params=params)

    def change_user_enabled(
            self,
            params: ChangeUserEnabledParamsModel,
            current_user_info: ValidateTokenResModel
    ):
        if current_user_info.user_category != "USER":
            raise BusinessError("没有权限")
        if params.id == current_user_info.res_user_id:
            raise BusinessError("不能修改自己的状态")
        user = self.__web_user_repository.get_by_id(user_id=params.id)
        if not user:
            raise BusinessError("用户不存在")
        user.enabled = params.enabled
        self.__web_user_repository.update(model=user)

    def get_user_detail(self, user_id: str):
        user = self.__web_user_repository.get_detail(user_id=user_id)
        if not user:
            raise BusinessError("用户不存在")
        if user.avatar_file_info:
            bucket_name = user.avatar_file_info.bucket_name
            object_name = user.avatar_file_info.object_name
            if bucket_name and object_name:
                user.avatar_file_info.url = self.__minio_client.get_file_url(
                    bucket_name=user.avatar_file_info.bucket_name,
                    object_name=user.avatar_file_info.object_name
                )
        return user

    def reset_password(
            self,
            params: ResetWebUserPasswordModel,
            current_user_info: ValidateTokenResModel,
            space: str = 'WEB'
    ):
        user_id = params.user_id
        user = self.__web_user_repository.get_by_id(user_id=user_id)
        if not user:
            raise BusinessError("用户不存在")
        user_info = self.__web_user_repository.get_info(user_id=user.id)
        role_code_list = [role.role_code.value for role in user_info.role_list]
        if EnumRoleCode.SUPER_ADMIN.value in role_code_list:
            if current_user_info.current_role_code != EnumRoleCode.SUPER_ADMIN.value:
                raise BusinessError("没有权限")
        sha256_hash = hashlib.sha256()
        password = secrets.token_urlsafe(12)
        salt = secrets.token_hex(16)
        sha256_hash.update((password + salt).encode('utf-8'))
        hash_value = sha256_hash.hexdigest()
        user.password_hash = hash_value
        user.password_salt = salt
        self.__web_user_repository.update(model=user)
        user_category = "WECOM_USER" if space == 'WECOM' else "WEB_USER"
        self.user_logout(user_id=user_id, user_category=user_category)
        return password

    def reset_self_password(
            self,
            params: ResetWebUserSelfPasswordModel,
            current_user_info: ValidateTokenResModel,
            space: str = 'WEB'
    ):
        user = self.__web_user_repository.get_user_by_union_user_id(
            union_user_id=current_user_info.union_user_info.id
        )
        if not user:
            raise BusinessError("用户不存在")

        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        if now - user.updated_at > timedelta(days=1):
            user.try_count = 0
            self.__web_user_repository.update(model=user)
        else:
            if user.try_count >= 5:
                raise BusinessError("尝试次数过多，请明天再试")

        # 验证是否和原密码一致
        self.check_password_old_vs_new(
            user=user,
            old_password=params.old_password,
            new_password=params.new_password
        )

        if params.new_password != params.new_password_repeat:
            raise BusinessError("两次输入新密码不一致")

        sha256_hash = hashlib.sha256()
        salt = secrets.token_hex(16)
        sha256_hash.update((params.new_password + salt).encode('utf-8'))
        hash_value = sha256_hash.hexdigest()
        user.password_hash = hash_value
        user.password_salt = salt
        user.reset_password = False
        self.__web_user_repository.update(model=user)
        user_category = "WECOM_USER" if space == 'WECOM' else "WEB_USER"
        self.user_logout(user_id=user.id, user_category=user_category)

    def check_password_old_vs_new(
            self,
            user: WebUserModel,
            old_password: str,
            new_password: str,
    ):
        sha256_hash = hashlib.sha256()
        sha256_hash.update((old_password + user.password_salt).encode('utf-8'))
        hash_value = sha256_hash.hexdigest()
        if hash_value != user.password_hash:
            user.try_count += 1
            self.__web_user_repository.update(model=user)
            raise BusinessError(f"原密码错误，还有{5 - user.try_count}次机会")

        if old_password == new_password:
            raise BusinessError("新密码不能和原密码一样")

    def register(
            self,
            params: UserRegisterParamsModel
    ):
        if not params.validate_auth_code or not params.captcha_id:
            raise BusinessError("请先进行安全验证")
        validate_auth_code_redis = self.__redis_client.get_value(
            key=f"captcha_validate_auth_code_{params.captcha_id}"
        )
        if validate_auth_code_redis != params.validate_auth_code:
            raise BusinessError(code=50001, message='安全验证失效，请重新进行验证')

        if not params.invite_code:
            raise BusinessError('邀请码不能为空')

        self.__invite_code_service.check_invite_code(
            invite_code=params.invite_code
        )
        exist = self.__web_user_repository.get_by_name(
            name=params.name
        )
        if exist:
            raise BusinessError("用户已存在")
        password_salt = secrets.token_hex(16)
        sha256_hash = hashlib.sha256()
        sha256_hash.update((params.password + password_salt).encode('utf-8'))
        hash_value = sha256_hash.hexdigest()
        user_id = str(uuid.uuid4())
        user = WebUserModel(
            id=user_id,
            name=params.name,
            mobile=None,
            email=None,
            enabled=True,
            avatar_file_info=None,
            password_salt=password_salt,
            password_hash=hash_value,
            try_count=0
        )
        self.__web_user_repository.insert(
            model=user
        )

        union_user_id = str(uuid.uuid4())
        self.__union_user_repository.insert(
            model=UnionUserModel(
                id=union_user_id,
                name=params.name,
                enabled=True,
                is_deleted=False,
            )
        )

        self.__union_user_user_repository.insert(
            model=UnionUserUserModel(
                union_user_id=union_user_id,
                union_user_user_category=EnumUnionUserCategory.WEB_USER.value,
                union_user_user_id=user_id,
            )
        )

        role = self.__role_repository.get_by_code(
            code=EnumRoleCode.WEB_USER.value,
        )
        self.__user_role_repository.insert(
            model=UserRoleModel(
                user_id=user_id,
                user_category=EnumUserRoleCategory.WEB_USER.value,
                role_id=role.id,
            )
        )
        self.__invite_code_service.update_register_num(
            invite_code=params.invite_code
        )

    def save_web_user(
            self,
            union_user_uuid: str,
            user_info: Dict
    ):
        exist_web_user = self.__web_user_repository.get_user_by_union_user_id(
            union_user_id=union_user_uuid
        )
        if exist_web_user:
            return
        web_user_id = str(uuid.uuid4())
        password_salt = secrets.token_hex(16)
        sha256_hash = hashlib.sha256()
        password_random = self.__tools_service.generate_secure_key(12)
        sha256_hash.update((password_random + password_salt).encode('utf-8'))
        hash_value = sha256_hash.hexdigest()
        name = user_info.get('name')
        if name is None or name.strip() == '':
            now = datetime.now()
            formatted_time = now.strftime("%Y%m%d_%H%M_%H%M%S_") + f"{now.microsecond // 1000:03d}"
            name = f"user_{formatted_time}_{self.__tools_service.generate_secure_key(6)}"
        user = WebUserModel(
            id=web_user_id,
            name=name,
            mobile=None,
            email=None,
            enabled=True,
            avatar_file_info=UploadResModel(),
            password_salt=password_salt,
            password_hash=hash_value,
            try_count=0,
            reset_password=True
        )
        exist_user_role = self.__user_role_repository.get_by_user_id(
            user_id=web_user_id
        )
        if not exist_user_role:
            role = self.__role_repository.get_by_code(
                code=EnumRoleCode.WEB_USER.value,
            )
            self.__user_role_repository.insert(
                model=UserRoleModel(
                    user_id=web_user_id,
                    user_category=EnumUserRoleCategory.WEB_USER.value,
                    role_id=role.id,
                )
            )
        self.__web_user_repository.insert(
            model=user
        )
        self.__union_user_user_service.save_union_user_user(
            union_user_id=union_user_uuid,
            union_user_user_id=web_user_id,
            union_user_user_category=EnumUnionUserCategory.WEB_USER.value
        )
        self.__web_user_organization_service.save(
            web_user_id=web_user_id,
        )
        self.__web_user_dept_service.save(
            web_user_id=exist_web_user.id,
            user_info=user_info
        )

    def update_web_user(
            self,
            union_user_uuid: str,
            user_info: Dict
    ):
        exist_web_user = self.__web_user_repository.get_user_by_union_user_id(
            union_user_id=union_user_uuid
        )
        name = user_info.get('name')
        if exist_web_user and name is not None:
            if name.strip() != '':
                exist_web_user.name = name.strip()
                self.__web_user_repository.update(
                    model=exist_web_user
                )
            self.__web_user_organization_service.save(
                web_user_id=exist_web_user.id,
            )
            self.__web_user_dept_service.save(
                web_user_id=exist_web_user.id,
                user_info=user_info
            )

    def wecom_user_to_web_user(
            self,
    ):
        all_wecom_user = self.__web_user_repository.get_all_wecom_user()
        for wecom_user in all_wecom_user:
            exist = self.__web_user_repository.get_by_wecom_user_id(
                wecom_user_id=wecom_user.id
            )
            if not exist:
                web_user_id = str(uuid.uuid4())
                password_salt = secrets.token_hex(16)
                sha256_hash = hashlib.sha256()
                password_random = self.__tools_service.generate_secure_key(12)
                sha256_hash.update((password_random + password_salt).encode('utf-8'))
                hash_value = sha256_hash.hexdigest()
                model = WebUserModel(
                    id=web_user_id,
                    name=wecom_user.name,
                    mobile=None,
                    email=None,
                    enabled=True,
                    avatar_file_info=UploadResModel(),
                    password_salt=password_salt,
                    password_hash=hash_value,
                    try_count=0,
                    reset_password=False
                )
                self.__web_user_repository.insert(
                    model=model
                )
                self.save_user_role(
                    web_user_id=web_user_id,
                )
                self.save_union_user(
                    name=wecom_user.name,
                    web_user_id=web_user_id,
                    wecom_user_id=wecom_user.id,
                )
                self.sava_web_user_organization(
                    web_user_id=web_user_id,
                )
                self.sava_web_user_dept(
                    web_user_id=web_user_id,
                    wecom_dept_id_list=wecom_user.department_ids if wecom_user.department_ids else wecom_user.raw_data.get('department', [])
                )

    def save_user_role(
            self,
            web_user_id: str,
    ):
        role = self.__role_repository.get_by_code(
            code=EnumRoleCode.WEB_USER.value,
        )
        self.__user_role_repository.insert(
            model=UserRoleModel(
                user_id=web_user_id,
                user_category=EnumUserRoleCategory.WEB_USER.value,
                role_id=role.id,
            )
        )

    def save_union_user(
            self,
            name: str,
            web_user_id: str,
            wecom_user_id: str,
    ):
        union_user_id = str(uuid.uuid4())
        self.__union_user_repository.insert(
            model=UnionUserModel(
                id=union_user_id,
                name=name,
                enabled=True,
                is_deleted=False,
            )
        )
        self.__union_user_user_service.save_union_user_user(
            union_user_id=union_user_id,
            union_user_user_id=web_user_id,
            union_user_user_category=EnumUnionUserCategory.WEB_USER.value
        )
        self.__union_user_user_service.save_union_user_user(
            union_user_id=union_user_id,
            union_user_user_id=wecom_user_id,
            union_user_user_category=EnumUnionUserCategory.WECOM_USER.value
        )
        return union_user_id

    def sava_web_user_organization(
            self,
            web_user_id: str,
    ):
        organization = self.__organization_repository.get_by_code(
            code=self.__config.get('ww', {}).get('organization_code', 'default')
        )
        if organization:
            exist = self.__web_user_organization_repository.get_exist(
                web_user_id=web_user_id,
                organization_id=organization.id
            )
            if not exist:
                self.__web_user_organization_repository.insert(
                    model=WebUserOrganizationModel(
                        web_user_id=web_user_id,
                        organization_id=organization.id
                    )
                )

    def sava_web_user_dept(
            self,
            web_user_id: str,
            wecom_dept_id_list: List[int],
    ):
        for dept_id in wecom_dept_id_list:
            dept = self.__dept_repository.get_by_wecom_dept_id(wecom_dept_id=dept_id)
            if dept:
                exist = self.__web_user_dept_repository.get_exist(
                    web_user_id=web_user_id,
                    dept_id=dept.id
                )
                if not exist:
                    self.__web_user_dept_repository.insert(
                        model=WebUserDeptModel(
                            web_user_id=web_user_id,
                            dept_id=dept.id
                        )
                    )

    def delete_by_union_user_id(self, union_user_id: str):
        web_user = self.__web_user_repository.get_user_by_union_user_id(
            union_user_id=union_user_id
        )
        if web_user:
            self.__web_user_organization_service.delete_by_web_user_id(
                web_user_id=web_user.id
            )
            self.__web_user_dept_service.delete_by_web_user_id(
                web_user_id=web_user.id
            )
            self.__user_role_service.delete_by_user_id(
                user_id=web_user.id
            )
            self.__web_user_repository.delete_by_id(
                data_id=web_user.id
            )
