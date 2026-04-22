# MOBILE 端约定

## 总则

- 样式：Tailwind CSS + SCSS，搜索框不加 `paddingLeft`
- 语法：Vue `<script setup>` 语法糖
- API 调用：`.then()` 链式写法，**不用** `async/await`
- 不加分号
- `if` / `else` 块体必须换行写大括号，禁止单行写法（如 `if (...) xxx;`）
- `.then()` / `.catch()` / `.finally()` 回调体换行写，禁止压缩成单行
- 组件库：Vant

## api 约定

详见 [API.md](API.md)
