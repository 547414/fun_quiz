from basic_module.model.backend_api_model import ChangeBackendApiIgnoreAuthParamsModel, BackendApiPageParamsModel
from basic_module.repository.backend_api_repository import BackendApiRepository


class BackendApiService:
    def __init__(
            self,
            backend_api_repository: BackendApiRepository,
    ):
        self.__backend_api_repository = backend_api_repository

    def get_backend_api_page(self, params: BackendApiPageParamsModel):
        return self.__backend_api_repository.get_backend_api_page(
            params=params
        )

    def change_backend_api_ignore_auth(
            self,
            params: ChangeBackendApiIgnoreAuthParamsModel
    ):
        model = self.__backend_api_repository.get_backend_api_by_id(
            backend_api_id=params.id
        )
        model.ignore_auth = params.ignore_auth
        self.__backend_api_repository.update(
            model=model
        )
