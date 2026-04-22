# UI Style and A11y Checklist

适用范围：`next/src` 前端页面与组件。  
目标风格：圆角、现代、青春、多彩、立体阴影。

## 设计一致性清单

- [x] 圆角一致性：主要控件统一 `rounded-xl` 及以上。
- [x] 阴影层级一致性：基础/悬浮/弹层使用 `--shadow-*` token。
- [x] 交互反馈一致性：按钮与可点击卡片存在 hover/active 层级变化。
- [x] 语义色一致性：success/warning/info/danger 颜色在 Badge/Button 中可复用。
- [x] 布局一致性：管理端与测验端均采用统一容器风格与留白节奏。

## 可访问性清单

- [x] 输入组件可见 focus ring（`focus-visible:ring-*`）。
- [x] 主要文本与背景保持可读性（避免高饱和低对比组合）。
- [x] 错误/告警信息可被快速识别（语义色 + 文案并存）。
- [x] 动效轻量，不影响内容阅读与操作节奏。
- [ ] 后续补充自动化视觉回归（建议 Playwright screenshot baseline）。

## 本轮执行记录（2026-04-22）

- 已完成 token 基线与 UI 原子组件统一升级。
- 已完成管理端壳层/模板层样式收口。
- 已完成测验/H5 主流程页面收口，并抽取 `quiz-page-shell` 复用组件。
- 已更新 Cursor 风格规则：`.cursor/rules/50-next-ui-theme-youthful-modern.mdc`。
