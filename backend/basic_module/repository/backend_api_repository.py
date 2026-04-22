from typing import List, Optional

from sqlalchemy.orm import Session

from basic.model.pagination_model import Pagination
from basic.repository.base_repository import BaseRepository
from basic_module.entity.backend_api import BackendApiEntity
from basic_module.model.backend_api_model import BackendApiModel, BackendApiViewModel, BackendApiPageParamsModel
from basic_module.model.permission_assign_model import EnumPermissionAssignGrantType, EnumPermissionAssignGranteeType, \
    EnumPermissionAssignPolicy


class BackendApiRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)

    def insert(self, model: BackendApiModel):
        return self.add(
            model=model,
            entity=BackendApiEntity
        )

    def update(self, model: BackendApiModel):
        return self.update_entity(
            entity=BackendApiEntity,
            entity_id=model.id,
            model=model
        )

    def get_exist(self, url: str):
        sql = """
        SELECT *
        FROM ct_backend_api cba
        WHERE cba.url = :url
        """

        return self.get_by_params(
            sql=sql,
            model=BackendApiModel,
            params={
                "url": url
            }
        )

    def get_backend_api_page(
            self,
            params: BackendApiPageParamsModel,
    ) -> Pagination:
        sql = """
        SELECT *
        FROM ct_backend_api cba
        WHERE cba.enabled IS TRUE
        """

        if params.search:
            sql += """
            AND cba.url LIKE :search
            """

        return self.get_page(
            sql=sql,
            data_model=BackendApiViewModel,
            page_index=params.page_index,
            page_size=params.page_size,
            search=None,
            search_fields=None,
            params={
                "search": f"%{params.search}%",
            }
        )

    def get_list(self) -> Optional[List[BackendApiModel]]:
        sql = """
        SELECT *
        FROM ct_backend_api cba
        WHERE cba.enabled IS TRUE
        """

        return self.get_all_by_params(
            sql=sql,
            model=BackendApiModel,
            params={}
        )

    def get_backend_api_by_id(self, backend_api_id: str) -> BackendApiModel:
        sql = """
        SELECT *
        FROM ct_backend_api cba
        WHERE cba.id = :backend_api_id
        """

        return self.get_by_params(
            sql=sql,
            model=BackendApiModel,
            params={
                "backend_api_id": backend_api_id
            }
        )

    def get_allow_backend_api(
            self,
            url: str,
            role_code: str
    ) -> Optional[BackendApiModel]:
        sql = """
        SELECT vba.*
        FROM view_backend_api vba
        INNER JOIN ct_permission_assign ca ON ca.grant_object_id = vba.id
        INNER JOIN ct_role cr ON cr.id = ca.grantee_object_id
        WHERE vba.enabled IS TRUE
        AND ca.grant_type::TEXT = :BACKEND_API
        AND ca.grantee_type::TEXT = :ROLE_GRANTEE_TYPE
        AND cr.code::TEXT = :role_code
        AND :url LIKE CONCAT(vba.cleaned_url, '%')
        AND ca.policy::TEXT = :ALLOW
        """

        return self.get_by_params(
            sql=sql,
            model=BackendApiModel,
            params={
                "url": f"{url}",
                "role_code": role_code,
                "BACKEND_API": EnumPermissionAssignGrantType.BACKEND_API.value,
                "ROLE_GRANTEE_TYPE": EnumPermissionAssignGranteeType.ROLE.value,
                "ALLOW": EnumPermissionAssignPolicy.ALLOW.value
            }
        )

    def get_by_url(self, url: str):
        sql = """
        SELECT *
        FROM view_backend_api vba
        WHERE :url LIKE CONCAT(vba.cleaned_url, '%')
        """

        return self.get_by_params(
            sql=sql,
            model=BackendApiModel,
            params={
                "url": f"{url}"
            }
        )
