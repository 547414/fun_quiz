import importlib
from datetime import datetime
from typing import Dict, TypeVar, Type, Optional, List, Any

from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from basic import BaseEntity
from basic.model.pagination_model import Pagination

# 创建两个类型变量
T_BaseModel = TypeVar('T_BaseModel', bound=BaseModel)
U_BaseEntity = TypeVar('U_BaseEntity', bound=BaseEntity)


class BaseRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(
            self,
            model: T_BaseModel,
            entity: Type[U_BaseEntity],
            commit_immediately: bool = False
    ) -> bool:
        """
        添加记录
        :param model: Pydantic模型类型
        :param entity: SQLAlchemy实体类型
        :param commit_immediately: 是否立即提交事务
        :return:
        """
        model.convert_names = False
        data_dict = model.model_dump()
        add_data = entity(**data_dict)
        self.session.add(add_data)
        if commit_immediately:
            self.session.commit()
        else:
            self.session.flush()  # 这里使用 flush 来立即执行 SQL 但不提交事务
        return True

    def get_model_by_id(
            self,
            entity_id: str,
            entity: Type[U_BaseEntity],
    ) -> Optional[T_BaseModel]:
        """
        根据 id 获取记录
        :param entity_id: 实体的ID
        :param entity: SQLAlchemy实体类型
        :return: Pydantic模型实例或None
        """
        data_dict = self.get_dict_by_id(
            entity_id=entity_id,
            entity=entity
        )
        if data_dict:
            # 从 entity 模块路径推导 model 模块路径
            entity_module = entity.__module__  # 获取 entity 所在模块
            model_module = entity_module.replace(".entity", ".model")  # 替换路径
            model_module = f"{model_module.lower()}_model"  # 添加模型文件名
            # 推断模型类名称
            model_class_name = entity.__name__.replace('Entity', '') + 'Model'
            try:
                # 动态导入模块
                models_module = importlib.import_module(model_module)
                # 获取模型类
                model_class = getattr(models_module, model_class_name, None)
                if model_class:
                    # 实例化模型类
                    model_instance = model_class(**data_dict)
                    return model_instance
                else:
                    print(f"未找到模型类 {model_class_name} 在模块 {model_module}")
            except ModuleNotFoundError as e:
                print(f"模块 {model_module} 导入失败: {e}")
        return None

    def get_dict_by_id(
            self,
            entity_id: str,
            entity: Type[U_BaseEntity]
    ) -> Optional[Dict]:
        """
        根据 id 获取记录
        :param entity_id: 实体的ID
        :param entity: SQLAlchemy实体类型
        :return: Dict或None
        """
        entity_instance = self.session.query(entity).filter_by(id=entity_id).first()
        if entity_instance:
            # 获取 entity 类中定义的字段名称
            column_names = {column.name for column in entity.__table__.columns}
            # 构造只包含 entity 中定义字段的字典
            data_dict = {key: value for key, value in entity_instance.__dict__.items() if key in column_names}
            return data_dict
        return None

    def get_all_by_id(
            self,
            model: T_BaseModel,
            entity_id: str
    ):
        """
        根据 id 获取所有记录
        :param model:
        :param entity_id:
        :return:
        """
        return self.session.query(model).filter_by(id=entity_id).all()

    def get_by_params(
            self,
            model: Type[T_BaseModel],
            entity: Type[U_BaseEntity] = None,
            params: Optional[Dict] = None,
            sql: Optional[str] = None,
    ) -> Optional[T_BaseModel]:
        """
        根据参数获取记录，并转换为指定的 Pydantic 模型
        :param entity: SQLAlchemy实体类型
        :param model: Pydantic模型类型
        :param params: 查询参数
        :param sql: 自定义SQL查询字符串
        :return: Pydantic模型列表
        """

        if sql:
            # 使用参数化查询执行自定义 SQL
            result = self.session.execute(text(sql), params=params)
            entities = result.fetchall()
            # 针对原生SQL查询结果进行处理
            model_data = model(**entities[0]._asdict()) if entities else None
        else:
            # 根据提供的 params 构建查询
            query = self.session.query(entity)
            if params:
                query = query.filter_by(**params)
            entities = query.all()
            # 将 SQLAlchemy 实体转换为字典，然后构造 Pydantic 模型
            model_data = None
            for ent in entities:
                entity_dict = {column.name: getattr(ent, column.name, None) for column in ent.__table__.columns}
                model_instance = model(**entity_dict)
                model_data = model_instance
                break

        return model_data

    def get_all_by_params(
            self,
            model: Type[T_BaseModel],
            entity: Type[U_BaseEntity] = None,
            params: Optional[Dict] = None,
            sql: Optional[str] = None,
    ) -> List[T_BaseModel]:
        """
        根据参数获取记录，并转换为指定的 Pydantic 模型
        :param entity: SQLAlchemy实体类型
        :param model: Pydantic模型类型
        :param params: 查询参数
        :param sql: 自定义SQL查询字符串
        :return: Pydantic模型列表
        """

        if sql:
            # 使用参数化查询执行自定义 SQL
            result = self.session.execute(text(sql), params=params)
            entities = result.fetchall()
            # 针对原生SQL查询结果进行处理
            model_list = [model(**row._asdict()) for row in entities]
        else:
            # 根据提供的 params 构建查询
            query = self.session.query(entity)
            if params:
                query = query.filter_by(**params)
            entities = query.all()
            # 将 SQLAlchemy 实体转换为字典，然后构造 Pydantic 模型
            model_list = []
            for ent in entities:
                entity_dict = {column.name: getattr(ent, column.name, None) for column in ent.__table__.columns}
                model_instance = model(**entity_dict)
                model_list.append(model_instance)

        return model_list

    def update_entity(
            self,
            model: T_BaseModel,
            entity_id: str,
            entity: Type[U_BaseEntity]
    ) -> bool:
        """
        更新记录
        :param model: Pydantic模型实例
        :param entity_id: 实体的ID
        :param entity: SQLAlchemy实体类型
        :return: 是否成功更新记录
        """
        # 通过ID查找现有记录
        entity_instance = self.session.query(entity).filter_by(id=entity_id).first()
        if not entity_instance:
            raise Exception(f"未找到 ID 为 {entity_id} 的 {entity.__name__} 实体")

        # 将Pydantic模型的数据转换为字典
        model.convert_names = False
        model.updated_at = datetime.now()
        update_data = model.model_dump()

        # 更新现有记录的字段值
        for key, value in update_data.items():
            setattr(entity_instance, key, value)

        # 提交更改
        self.session.commit()
        return True

    def delete(self, entity: Type[U_BaseEntity], entity_id: str):
        """
        根据表名和 ID 删除记录
        :param entity: 实体类
        :param entity_id: 要删除的实体的 ID
        :return: None
        """
        table_name = entity.__tablename__  # 获取表名
        delete_sql = f"DELETE FROM {table_name} WHERE id = :entity_id"

        try:
            # 执行原生 SQL 语句删除记录
            self.session.execute(text(delete_sql), {'entity_id': entity_id})
            self.session.commit()
        except Exception as e:
            # 如果出错则回滚并抛出异常
            self.session.rollback()
            raise Exception(f"删除 ID 为 {entity_id} 的 {entity.__name__} 实体时出错: {e}")

    def execute_sql(self, sql, params: Dict):
        """
        执行 sql 语句并返回结果
        :param sql: SQL语句
        :param params: SQL参数
        :return: 查询结果
        """
        result = self.session.execute(text(sql), params)
        self.session.flush()

        # 如果是SELECT查询，返回所有结果
        if sql.strip().lower().startswith("select"):
            return result.fetchall()

        # 对于非SELECT查询，返回影响的行数
        else:
            return result.rowcount

    def get_page(
            self,
            sql: str,
            data_model: Type[T_BaseModel],
            page_index: int,
            page_size: int,
            order_by: Dict[str, bool] = None,
            filters: Dict[str, Any] = None,
            search: str = None,
            search_fields: List[str] = None,
            params: Optional[Dict] = None,
    ) -> Pagination:
        """
        根据给定的基础SQL语句、分页、排序和过滤参数执行分页查询。

        :param sql: 基础SQL查询语句，不应包含WHERE, ORDER BY和LIMIT部分
        :param data_model: Pydantic模型类型
        :param page_index: 请求的页码索引
        :param page_size: 每页大小
        :param order_by: 排序的字段和方向，格式为{字段名: True}，True表示升序，False表示降序
        :param filters: 过滤条件，格式为{字段名: 值}
        :param search: 搜索关键字
        :param search_fields: 需要进行搜索的字段列表
        :param params: 额外的查询参数
        :return: 包含分页信息和查询结果的字典
        """
        # 确保页码索引不为负数
        if page_index < 1:
            page_index = 1

        # 构建过滤条件
        filter_clause = ""
        filter_values = {}
        filter_conditions = []

        if filters:
            for field, value in filters.items():
                if isinstance(value, list):
                    if value:  # 列表非空
                        filter_conditions.append(f"{field} = ANY(:{field})")
                        filter_values[field] = value
                else:
                    if value is not None:
                        filter_conditions.append(f"{field} = :{field}")
                        filter_values[field] = value

        # 添加搜索条件
        if search and search_fields:
            search_conditions = [f"{field} LIKE :search" for field in search_fields]
            search_clause = " OR ".join(search_conditions)
            filter_conditions.append(f"({search_clause})")
            filter_values['search'] = f"%{search}%"

        if filter_conditions:
            filter_clause = " WHERE " + " AND ".join(filter_conditions)

        # 构建排序条件
        order_clause = ""
        if order_by:
            order_conditions = [f"{field} {'ASC' if asc else 'DESC'}" for field, asc in order_by.items()]
            order_clause = " ORDER BY " + ", ".join(order_conditions)

        # 完整的SQL查询语句
        complete_sql = f"{sql}{filter_clause}{order_clause} LIMIT :limit OFFSET :offset"

        # 分页参数
        page_values = {
            "limit": page_size,
            "offset": (page_index - 1) * page_size
        }

        # 合并参数
        query_params = {**filter_values, **page_values, **params}

        # 查询过滤后的总行数
        count_sql = f"SELECT COUNT(*) FROM ({sql}{filter_clause}) as sub"
        filter_count = self.session.execute(text(count_sql), query_params).scalar()

        # 查询总行数
        total_sql = f"SELECT COUNT(*) FROM ({sql}) as sub"
        total_count = self.session.execute(text(total_sql), query_params).scalar()

        # 获取数据并转换为字典
        result = self.session.execute(text(complete_sql), query_params).fetchall()
        data = [dict(row._mapping) for row in result]

        # 将结果转换为Pydantic模型实例
        data_models: List[T_BaseModel] = [data_model(**row) for row in data]

        # 构建返回数据
        return Pagination(
            page_index=page_index,
            page_size=page_size,
            total_count=total_count,
            filter_count=filter_count,
            data=data_models
        )
