from basic_module.basic_module_container import BasicModuleContainer
from config.config import Config

basic_module_container = BasicModuleContainer()
basic_module_container.config.from_dict(Config().model_dump())

basic_module_container.wire(packages=[__name__])
