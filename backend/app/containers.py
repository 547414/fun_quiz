from dependency_injector import containers, providers

from basic_module import BasicModuleContainer
from biz_module import BizModuleContainer


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    basic_module_container = providers.Container(BasicModuleContainer, config=config)
    biz_module_container = providers.Container(
        BizModuleContainer,
        basic_module_container=basic_module_container,
        config=config
    )
