# 后端约定

## 总则

- **分层**：`entity/` → `model/` → `repository/` → `service/` → `router/`
- **依赖注入**：`dependency-injector`，容器 `app/containers.py` → 各模块 `xxx_module_container.py`
- **配置**：`app_config.toml` 的 `settings.active` 决定环境，加载 `config/app_{env}_config.toml`
- **事务**：`UnitOfWork` 上下文管理器管理 SQLAlchemy session
- **类型约束**：`list` 用 `List`，`dict` 用 `Dict`（从 typing 导入）
- **SQL**：使用三引号包裹，三引号后和结束三引号前必须换行（拼接片段同理）
- **数据封装**：处理或取数据前用 model 封装，避免下划线/驼峰混乱
- **方法调用**：router/service/repository 中调用方法必须写明参数名（`func(param_name=value)`）
- **返回给前端**：数据格式 必须使用model封装

## 各层规范
``
- [ENTITY.md](ENTITY.md) — entity 层
- [MODEL.md](MODEL.md) — model 层
- [REPOSITORY.md](REPOSITORY.md) — repository 层
- [SERVICE.md](SERVICE.md) — service 层
- [ROUTER.md](ROUTER.md) — router 层
- [ENUM.md](ENUM.md) — 枚举
