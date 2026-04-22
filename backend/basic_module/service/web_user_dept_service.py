import os
from typing import Dict, Any

import toml

from basic_module.model.web_user_dept_model import WebUserDeptModel
from basic_module.repository.dept_repository import DeptRepository
from basic_module.repository.organization_repository import OrganizationRepository
from basic_module.repository.web_user_dept_repository import WebUserDeptRepository


class WebUserDeptService:
    def __init__(
            self,
            web_user_dept_repository: WebUserDeptRepository,
            organization_repository: OrganizationRepository,
            dept_repository: DeptRepository,
    ):
        self.__organization_repository = organization_repository
        self.__dept_repository = dept_repository

        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.__base_path = os.path.join(path, "../")
        self.__app_config = toml.load(fr"{self.__base_path}/app_config.toml")
        self.__active = self.__app_config.get('settings', {}).get('active', 'development')
        self.__config_name = f'app_{self.__active}_config.toml'
        self.__config = toml.load(fr"{self.__base_path}/config/{self.__config_name}")

    def save(self, web_user_id: str, user_info: Dict[str, Any]):
        dept_ids = user_info.get('info').get('department')
        if not dept_ids:
            dept_ids = []
        organization = self.__organization_repository.get_by_code(
            code=self.__config.get('ww', {}).get('organization_code', 'default')
        )
        if organization:
            for dept_id in dept_ids:
                wecom_dept = self.__wecom_dept_repository.get_exist_dept(
                    organization_id=organization.id,
                    dept_id=dept_id
                )
                if not wecom_dept:
                    continue
                dept = self.__dept_repository.get_by_source_id(
                    organization_id=organization.id,
                    source_id=wecom_dept.id,
                )
                exist = self.__web_user_dept_repository.get_exist(
                    web_user_id=web_user_id,
                    dept_id=dept.id,
                )
                if not exist and dept:
                    self.__web_user_dept_repository.insert(
                        model=WebUserDeptModel(
                            web_user_id=web_user_id,
                            dept_id=dept.id,
                        )
                    )

    def delete_by_web_user_id(self, web_user_id: str):
        exist_list = self.__web_user_dept_repository.get_list_by_web_user_id(
            web_user_id=web_user_id
        )
        if not exist_list:
            exist_list = []
        for exist in exist_list:
            self.__web_user_dept_repository.delete_by_id(
                data_id=exist.id
            )
