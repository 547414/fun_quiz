---
name: layered-feature-delivery
description: Implements features with strict layered design and clean code for Next.js fullstack with TypeScript, Tailwind CSS, and Neon. Use when adding pages, server actions, route handlers, data access modules, or fullstack business flows.
---

# Layered Feature Delivery

## Goal

在不破坏现有架构的前提下交付功能，保持可读、可测、可维护。

## Server Workflow

1. 定义输入输出类型，先固定 domain model 和 DTO。
2. 将 Neon 查询放入 `db/repository` 层，不在页面里直接查询。
3. 在 server action 或 route handler 中编排业务流程。
4. 校验参数与权限后再执行业务写操作。
5. 多步写操作显式设置事务边界，保证一致性。

## UI Workflow

1. 先拆页面职责：容器逻辑与展示逻辑分离。
2. API 或 server action 调用集中封装，避免散落在多个组件中。
3. 状态命名可读，避免缩写和无语义布尔值。
4. 复杂逻辑抽 hook，视图层保持 Tailwind 原子化和可读性。

## Clean Code Gates

- 单个函数应可被一句话描述职责。
- 同一层不依赖更高层实现细节。
- 任何重复逻辑出现第二次就评估抽取。
- 错误分支必须可观测、可定位、可追踪。
- 客户端组件不得直接访问 Neon 或泄露数据库细节。
- 依赖安装与脚本执行默认使用 `yarn` 命令。
