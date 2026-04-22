import os
import uuid
from datetime import timedelta, datetime, timezone, UTC
from enum import Enum
from typing import Dict

import jwt
import toml
from fastapi import HTTPException

from basic.api_response.api_response import ApiResponse
from basic.error.base_error import BusinessError
from basic.minio_client.minio_client import MinioClient
from basic.redis_client.redis_client import RedisClient
from basic_module.model.auth_model import JwtPayloadInfo
from basic_module.model.union_user_model import EditUnionUserInfoModel, UnionUserModel, \
    UnionUserAuthCodeLoginParamsModel, \
    RefreshUnionUserAccessTokenViewModel, DeleteUnionUserModel
from basic_module.model.union_user_user_model import EnumUnionUserCategory
from basic_module.model.validate_token_model import ValidateTokenResModel
from basic_module.repository.backend_api_repository import BackendApiRepository
from basic_module.repository.union_user_repository import UnionUserRepository
from basic_module.service.union_user_user_service import UnionUserUserService
from basic_module.service.web_user_service import WebUserService


class UnionUserService:
    def __init__(
            self,
            union_user_repository: UnionUserRepository,
            backend_api_repository: BackendApiRepository,
            union_user_user_service: UnionUserUserService,
            web_user_service: WebUserService,
            minio_client: MinioClient,
            redis_client: RedisClient,
    ):
        self.__union_user_repository = union_user_repository
        self.__backend_api_repository = backend_api_repository
        self.__union_user_user_service = union_user_user_service
        self.__web_user_service = web_user_service
        self.__minio_client = minio_client
        self.__redis_client = redis_client

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

    def auth_code_login(self, params: UnionUserAuthCodeLoginParamsModel, scene: str = "DEFAULT", space: str = "DEFAULT"):
        union_user_id = self.__redis_client.get_value(
            key=f"{params.auth_code}",
        )
        return self.generate_union_user_token(
            union_user_id=union_user_id,
            scene=scene,
            space=space
        )

    def edit_union_user_info(
            self,
            params: EditUnionUserInfoModel,
    ):
        union_user = self.__union_user_repository.get_by_id(
            union_user_id=params.union_user_id
        )

        if not union_user:
            raise BusinessError('用户不存在')
        union_user.name = params.name
        self.__union_user_repository.update(
            model=union_user
        )

    def save_union_user(
            self,
            union_user_user_id: str,
            wx_user_id: str,
            union_user_user_category: str,
            user_info: Dict
    ):
        exist_user = self.__wecom_user_repository.get_exist_user(
            user_id=wx_user_id,
        )
        union_user = self.__union_user_repository.get_exist_union_user(
            union_user_user_id=exist_user.id,
            union_user_user_category=union_user_user_category,
        )
        if not union_user:
            union_user_id = str(uuid.uuid4())
            self.__union_user_repository.insert(
                model=UnionUserModel(
                    id=union_user_id,
                    name=user_info.get('name'),
                    enabled=True,
                    is_deleted=False,
                )
            )
        else:
            union_user_id = union_user.id
            name = user_info.get('name')
            if name is not None:
                if name.strip() != '':
                    union_user.name = name.strip()
                    self.__union_user_repository.update(
                        model=union_user
                    )

        self.__union_user_user_service.save_union_user_user(
            union_user_id=union_user_id,
            union_user_user_id=union_user_user_id,
            union_user_user_category=union_user_user_category,
        )
        return union_user_id

    def get_union_user_info(self, union_user_id: str):
        union_user = self.__union_user_repository.get_union_user(
            union_user_id=union_user_id
        )
        union_user_user_info = self.__union_user_repository.get_user_info(
            user_id_list=union_user.user_id_list
        )
        union_user.union_user_user_info = union_user_user_info
        for user in union_user.user_list:
            role_data = union_user_user_info.role_data
            data_key = user.union_user_user_id.replace('-', '_')
            user.union_user_user_name = union_user.name
            if role_data:
                user.union_user_user_role_list = role_data.get(data_key).role_list if role_data.get(data_key) else []
                if len(user.union_user_user_role_list) > 0:
                    user.current_role_code = user.union_user_user_role_list[0].role_code
                    break
        return union_user

    def generate_union_user_token(
            self,
            union_user_id: str,
            scene: str = "DEFAULT",
            space: str = "DEFAULT",
    ):
        jwt_payload = JwtPayloadInfo(
            union_user_info=self.get_union_user_info(union_user_id=union_user_id),
        )
        return self.__web_user_service.generate_user_token(
            jwt_payload=jwt_payload,
            scene=scene,
            space=space
        )

    def __create_access_token(self, data: JwtPayloadInfo) -> str:
        """生成短期有效的 Access Token"""
        data.convert_names = False
        to_encode = data.model_dump().copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.__config['jwt']['ACCESS_TOKEN_EXPIRE_MINUTES'])
        # expire = datetime.now(timezone.utc) + timedelta(minutes=1)

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
        expire = datetime.now(timezone.utc) + timedelta(days=self.__config['jwt']['REFRESH_TOKEN_EXPIRE_DAYS'])
        # expire = datetime.now(timezone.utc) + timedelta(minutes=2)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            self.__config['jwt']['SECRET_KEY'],
            algorithm=self.__config['jwt']['ALGORITHM']
        )
        return encoded_jwt

    def validate_token(
            self,
            token: str,
            url: str = None,
            token_type: str = None,
            space: str = 'DEFAULT',
            scene: str = "DEFAULT"
    ):
        """验证 Token 是否有效，检查是否在黑名单中"""
        try:
            if not token_type:
                token_type = self.__config['jwt']['TOKEN_TYPE']
            # 检查 Token 是否已被加入黑名单
            if self.is_token_revoked(token, token_type):
                raise HTTPException(status_code=401, detail=self.__revoked_detail)

            # 获取 Token 中的category字段
            payload = jwt.decode(
                token,
                self.__config['jwt']['SECRET_KEY'],
                algorithms=[self.__config['jwt']['ALGORITHM']]
            )
            payload = JwtPayloadInfo(**payload)
            exp = payload.exp

            # 检查 Token 是否已过期
            if exp is None or datetime.fromtimestamp(exp, UTC) < datetime.now(UTC):
                raise HTTPException(status_code=401, detail=self.__expired_detail)

            access_token = self.__redis_client.get_value(f"access_token_{space}:{payload.union_user_info.id}_{scene}")
            if access_token is None or access_token != token:
                raise HTTPException(status_code=401, detail=self.__invalid_detail)

            current_user_info = ValidateTokenResModel(
                union_user_info=payload.union_user_info
            )
            for user in payload.union_user_info.user_list:
                role_data = payload.union_user_info.union_user_user_info.role_data
                data_key = user.union_user_user_id.replace('-', '_')
                user.union_user_user_name = payload.union_user_info.name
                if role_data:
                    if role_data.get(data_key):
                        user.union_user_user_role_list = role_data.get(data_key).role_list
                    else:
                        user.union_user_user_role_list = []
                else:
                    user.union_user_user_role_list = []
                if user.union_user_user_category == EnumUnionUserCategory.WEB_USER.value:
                    current_user_info.current_user = user
                    current_user_info.current_role_code = user.current_role_code
            return current_user_info
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail=self.__expired_detail)
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail=self.__invalid_detail)

    def is_token_revoked(self, token: str, token_type: str) -> bool:
        """检查 Token 是否在黑名单中"""
        return self.__redis_client.get_value(f"blacklist:{token_type}_token:{token}") is not None

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

    def refresh_access_token(self, refresh_token: str, space: str = 'WEB', scene: str = "DEFAULT",):
        """使用 refresh_token 刷新 access_token"""
        try:
            # 验证 refresh_token 是否在黑名单中
            if self.is_token_revoked(refresh_token, "refresh"):
                raise HTTPException(status_code=401, detail=self.__refresh_revoked_detail)

            # 验证 refresh_token 的有效性
            payload = jwt.decode(
                refresh_token,
                self.__config['jwt']['SECRET_KEY'],
                algorithms=[self.__config['jwt']['ALGORITHM']]
            )
            payload = JwtPayloadInfo(**payload)

            jwt_payload = JwtPayloadInfo(
                union_user_info=payload.union_user_info
            )
            new_access_token = self.__create_access_token(data=jwt_payload)

            # 将新的 access_token 更新到 Redis
            self.__redis_client.set_value(
                f"access_token_{space}:{payload.union_user_info.id}_{scene}",
                new_access_token,
                expiration=int(timedelta(minutes=self.__config['jwt']['ACCESS_TOKEN_EXPIRE_MINUTES']).total_seconds())
            )

            return RefreshUnionUserAccessTokenViewModel(
                access_token=new_access_token,
                token_type=self.__config['jwt']['TOKEN_TYPE']
            )

        except jwt.ExpiredSignatureError:
            detail = ApiResponse(code=40101, message=self.__refresh_expired_detail)
            raise HTTPException(status_code=401, detail=detail)
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail=self.__refresh_invalid_detail)

    def logout(
            self,
            current_user_info: ValidateTokenResModel,
            space: str = 'WEB',
    ):
        user_category = 'WECOM_USER'
        if space == 'WEB':
            user_category = 'WEB_USER'

        access_token = self.__redis_client.get_value(
            f"access_token_{user_category}:{current_user_info.union_user_info.id}"
        )
        if access_token:
            self.__redis_client.delete_key(
                key=f"access_token_{user_category}:{current_user_info.union_user_info.id}"
            )

        refresh_token = self.__redis_client.get_value(
            f"refresh_token_{user_category}:{current_user_info.union_user_info.id}"
        )
        if refresh_token:
            self.__redis_client.delete_key(
                key=f"refresh_token_{user_category}:{current_user_info.union_user_info.id}"
            )

    def delete(self, params: DeleteUnionUserModel):
        union_user = self.__union_user_repository.get_by_id(
            union_user_id=params.union_user_id
        )
        if not union_user:
            raise BusinessError('用户不存在')

        self.__web_user_service.delete_by_union_user_id(
            union_user_id=params.union_user_id
        )

        self.__union_user_user_service.delete_by_union_user_id(
            union_user_id=params.union_user_id
        )

        self.__union_user_repository.delete_by_id(
            data_id=params.union_user_id
        )
