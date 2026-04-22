from biz_module.biz_module_container import BizModuleContainer
from config.config import Config

biz_module_container = BizModuleContainer()
_config = Config().model_dump()
biz_module_container.config.from_dict(_config)
biz_module_container.basic_module_container.config.from_dict(_config)  # 内部 basic_module_container 也需要 DB config

biz_module_container.wire(packages=[__name__])
