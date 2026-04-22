---
name: clean-code-review
description: Reviews repository changes for clean code, layering boundaries, readability, and regression risk. Use when the user asks for review, code quality audit, refactor check, or merge readiness.
---

# Clean Code Review

## Scope

- 关注正确性、可维护性、边界清晰度、重复代码和异常处理。
- 先报高风险问题，再给中低优先级改进建议。

## Review Workflow

1. 识别改动涉及的 Next.js 模块边界（UI、server action、route handler、db 层）。
2. 检查命名、函数长度、嵌套层级、重复逻辑。
3. 检查错误处理是否吞异常、是否可定位。
4. 检查是否存在跨层耦合、客户端直连数据库、隐藏副作用。
5. 输出按严重级排序的问题清单。

## Output Format

- `Critical`: 必须修复，说明风险与触发场景。
- `Major`: 建议尽快修复，说明长期维护成本。
- `Minor`: 可选优化，给出更清晰写法。

## Project Anchors

- 技术栈为 `Next.js 全栈 + TypeScript + Tailwind CSS + Neon`。
- 包管理器默认使用 `yarn`，评审命令与文档示例保持一致。
- 数据访问仅允许在服务端边界，客户端组件禁止直接触库。
- 代码评审优先关注分层边界、类型约束、数据库一致性风险。
