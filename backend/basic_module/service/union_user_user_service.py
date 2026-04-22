from basic_module.model.union_user_user_model import UnionUserUserModel
from basic_module.repository.union_user_user_repository import UnionUserUserRepository
from basic_module.repository.web_user_repository import WebUserRepository
from basic_module.service.user_role_service import UserRoleService


class UnionUserUserService:
    def __init__(
            self,
            union_user_user_repository: UnionUserUserRepository,
            user_role_service: UserRoleService,
            web_user_repository: WebUserRepository,
    ):
        self.__union_user_user_repository = union_user_user_repository
        self.__user_role_service = user_role_service
        self.__web_user_repository = web_user_repository

    def edit_web_user_relation(
            self,
            user_id: str,
            union_user_uuid: str,
    ):
        exist = self.__union_user_user_repository.get_web_user_exist(
            web_user_id=user_id,
        )
        if exist:
            exist.union_user_id = union_user_uuid
            self.__union_user_user_repository.update(
                model=exist
            )
        else:
            self.__union_user_user_repository.insert(
                model=UnionUserUserModel(
                    union_user_id=union_user_uuid,
                    union_user_user_category="WEB_USER",
                    union_user_user_id=user_id,
                )
            )

    def edit_wx_user_relation(
            self,
            wx_user_id: str,
            union_user_uuid: str
    ):
        exist = self.__union_user_user_repository.get_wx_user_exist(
            wx_user_id=wx_user_id,
        )
        if exist:
            exist.union_user_id = union_user_uuid
            self.__union_user_user_repository.update(
                model=exist
            )
        else:
            self.__union_user_user_repository.insert(
                model=UnionUserUserModel(
                    union_user_id=union_user_uuid,
                    union_user_user_category="WECHAT_OFFICIAL_ACCOUNT",
                    union_user_user_id=wx_user_id,
                )
            )

    def get_wx_user_id_by_union_user_id(self, union_user_id: str):
        union_user_user = self.__union_user_user_repository.get_wx_user(
            union_user_id=union_user_id,
        )
        if union_user_user:
            return union_user_user.wx_user_id
        return None

    def save_union_user_user(
            self,
            union_user_id: str,
            union_user_user_id: str,
            union_user_user_category: str,
    ):
        exist = self.__union_user_user_repository.get_union_user_user_exist(
            union_user_id=union_user_id,
            union_user_user_category=union_user_user_category,
        )
        if not exist:
            self.__union_user_user_repository.insert(
                model=UnionUserUserModel(
                    union_user_id=union_user_id,
                    union_user_user_category=union_user_user_category,
                    union_user_user_id=union_user_user_id,
                )
            )
        else:
            exist.union_user_user_id = union_user_user_id
            self.__union_user_user_repository.update(
                model=exist
            )

    def delete_by_union_user_id(self, union_user_id: str):
        exist_list = self.__union_user_user_repository.list_by_union_user_id(
            union_user_id=union_user_id
        )
        if not exist_list:
            exist_list = []
        for exist in exist_list:
            exist_web_user = self.__web_user_repository.get_by_id(
                user_id=exist.union_user_user_id
            )
            if exist_web_user:
                self.__web_user_repository.delete_by_id(
                    data_id=exist_web_user.id
                )
            self.__union_user_user_repository.delete_by_id(
                data_id=exist.id
            )
            self.__user_role_service.delete_by_user_id(
                user_id=exist.union_user_user_id
            )
