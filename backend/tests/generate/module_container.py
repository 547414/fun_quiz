import os


def test_generate_module_container():
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_path = os.path.join(path, "../")
    # module_name = "common_workflow_module"
    module_name = "biz_module"

    table_name_lower_list = []

    entity_path = f"{base_path}/{module_name}/entity"
    for file_name in os.listdir(entity_path):
        if file_name == "__init__.py":
            continue
        if file_name == "__pycache__":
            continue
        table_name_lower_list.append(file_name.replace(".py", ""))

    import_content = ""
    repository_content = ""
    service_content = ""

    # 后续添加了新表，再调用此方法生成模板只生成新添加表的
    table_name_lower_list = [
        'goods_permission',
    ]

    for table_name_lower in table_name_lower_list:
        table_name = "".join(word.capitalize() for word in table_name_lower.split("_"))

        import_content += f"""
from {module_name}.repository.{table_name_lower}_repository import {table_name}Repository
from {module_name}.service.{table_name_lower}_service import {table_name}Service"""
        repository_content += f"""

{table_name_lower}_repository = providers.Factory(
       {table_name}Repository,
       session=session,
)"""
        service_content += f"""

{table_name_lower}_service = providers.Factory(
        {table_name}Service,
        {table_name_lower}_repository={table_name_lower}_repository,
)"""

    output_directory = f"{base_path}/{module_name}/service"
    output_file_name = f"{base_path}/temp/temp_module_container"
    os.makedirs(output_directory, exist_ok=True)

    output_file_path = os.path.join(output_directory, output_file_name)

    content = import_content + repository_content + service_content

    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"文件已处理并保存到: {output_file_path}")
