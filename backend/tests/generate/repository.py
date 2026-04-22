import os
import re


def test_generate_repository():
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

    # 后续添加了新表，再调用此方法生成模板只生成新添加表的
    table_name_lower_list = [
        'goods_permission',
    ]

    for table_name_lower in table_name_lower_list:
        table_name = "".join(word.capitalize() for word in table_name_lower.split("_"))

        input_file_path = f"{base_path}/tests/generate/template_repository"

        output_directory = f"{base_path}/{module_name}/repository"
        output_file_name = f"{table_name_lower}_repository.py"

        os.makedirs(output_directory, exist_ok=True)

        with open(input_file_path, "r", encoding="utf-8") as file:
            content = file.read()

        pattern_lower = re.escape("[TABLE_NAME_LOWER]")
        pattern_upper = re.escape("[TABLE_NAME]")
        pattern_module_name = re.escape("[MODULE_NAME]")

        content = re.sub(pattern_lower, table_name_lower, content)
        content = re.sub(pattern_upper, table_name, content)
        content = re.sub(pattern_module_name, module_name, content)

        output_file_path = os.path.join(output_directory, output_file_name)

        with open(output_file_path, "w", encoding="utf-8") as file:
            file.write(content)

        print(f"文件已处理并保存到: {output_file_path}")
