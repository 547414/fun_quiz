import os

import toml

from basic_module.model.web_user_organization_model import WebUserOrganizationModel
from basic_module.repository.organization_repository import OrganizationRepository
from basic_module.repository.web_user_organization_repository import WebUserOrganizationRepository


class WebUserOrganizationService:
    def __init__(
            self,
            web_user_organization_repository: WebUserOrganizationRepository,
            organization_repository: OrganizationRepository,
    ):
        self.__web_user_organization_repository = web_user_organization_repository
        self.__organization_repository = organization_repository

        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.__base_path = os.path.join(path, "../")
        self.__app_config = toml.load(fr"{self.__base_path}/app_config.toml")
        self.__active = self.__app_config.get('settings', {}).get('active', 'development')
        self.__config_name = f'app_{self.__active}_config.toml'
        self.__config = toml.load(fr"{self.__base_path}/config/{self.__config_name}")

    def save(self, web_user_id: str):
        organization = self.__organization_repository.get_by_code(
            code=self.__config.get('ww', {}).get('organization_code', 'default')
        )
        if organization:
            exist = self.__web_user_organization_repository.get_exist(
                web_user_id=web_user_id,
                organization_id=organization.id,
            )
            if not exist:
                self.__web_user_organization_repository.insert(
                    model=WebUserOrganizationModel(
                        web_user_id=web_user_id,
                        organization_id=organization.id,
                    )
                )

    def delete_by_web_user_id(self, web_user_id: str):
        exist_list = self.__web_user_organization_repository.get_list_by_web_user_id(
            web_user_id=web_user_id
        )
        if not exist_list:
            exist_list = []
        for exist in exist_list:
            self.__web_user_organization_repository.delete_by_id(
                data_id=exist.id
            )
