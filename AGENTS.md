# Repository Guidelines

## 工作规范

- 不要全量扫描项目（初始化除外）
- 用简体中文回答，代码外的回答要精炼
- 完成后只告知修改了哪些文件
- 无指定时不输出测试/部署/说明文档

## 项目概览

各种趣味测验的用户端、管理端。


## 目录结构

```
backend/
├── app/              # 路由自动注册（*_router.py → /api/{模块名}）
│   └── containers.py # DI 容器入口
├── basic/            # 基础设施（BaseEntity/BaseRepository/UoW/Minio/Redis）
├── basic_module/     # 核心业务（org/user/role/permission/wecom）
├── biz_module/       # 自定义业务（可扩展）
├── config/           # Pydantic BaseSettings + TOML
└── run.py
web/                  # Vue 3 + Vite + Naive UI + Tailwind（PC）
mobile/               # Vue 3 + Vite + Vant + Tailwind（移动端）
```

## 技术栈

后端：FastAPI · SQLAlchemy 2.0 · PostgreSQL · Redis · MinIO · Celery · LangChain
前端：Vue 3 · Vite · Pinia · Naive UI（PC）· Vant（移动端）· Tailwind CSS · SCSS · 语法糖

## 后端约定

详见 `code_config/backend/BACKEND.md`（总则 + 各层子文件索引）

## WEB端约定

详见 `code_config/web/WEB.md`

## MOBILE端约定

详见 `code_config/mobile/MOBILE.md`
