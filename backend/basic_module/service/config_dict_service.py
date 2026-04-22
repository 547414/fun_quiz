from basic_module.repository.config_dict_repository import ConfigDictRepository


class ConfigDictService:
    def __init__(
            self,
            config_dict_repository: ConfigDictRepository,
    ):
        self.__config_dict_repository = config_dict_repository
