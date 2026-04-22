import os
import importlib
import types
from pydantic import BaseModel

from basic import BaseEntity
import biz_module.entity as biz_module
import basic_module.entity as basic_module_entity_module
import basic.entity as basic_entity_module
from basic_module import basic_module_container


class ModuleData(BaseModel):
    module: types.ModuleType
    module_name: str

    class Config:
        arbitrary_types_allowed = True


def generate_data_table(module_data: ModuleData):
    entity_module_path = os.path.dirname(module_data.module.__file__)

    if not os.path.exists(entity_module_path):
        raise FileNotFoundError(f"Path {entity_module_path} does not exist.")

    for filename in os.listdir(entity_module_path):
        if filename.endswith('.py') and filename != '__init__.py' and filename != 'basic_entity.py':
            module_name = f'{module_data.module_name}.entity.{filename[:-3]}'
            try:
                importlib.import_module(module_name)
                print(f'Successfully imported {module_name}')
            except ImportError as e:
                print(f'Error importing {module_name}: {e}')


def test_generate_data_table():
    entity_modules = [
        ModuleData(
            module=biz_module,
            module_name='biz_module'
        ),
        ModuleData(
            module=basic_entity_module,
            module_name='basic'
        ),
        ModuleData(
            module=basic_module_entity_module,
            module_name='basic_module'
        )
    ]
    for module in entity_modules:
        generate_data_table(module)

    # 创建表
    BaseEntity.metadata.create_all(basic_module_container.engine())
