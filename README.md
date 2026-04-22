# Fun Quiz

一个开箱即用的趣味测验平台，支持多种算法类型（MBTI/SBTI 风格向量匹配、累分段映射、分支跳题、加权随机），内置 Token 授权管理和
AI 辅助创建。

## 功能特性

- **四种测验算法**
    - `vector` — 多维向量匹配（适合 MBTI / SBTI 等人格测验）
    - `score` — 累分段映射（适合偏好/能力测评）
    - `branch` — 分支跳题决策树（适合分类诊断）
    - `random` — 加权随机（适合趣味抽签类）
- **Token 授权体系** — 后台批量生成访问令牌，支持限次/限期/无限次，用户凭链接即可作答，无需注册登录
- **AI 辅助创建** — 粘贴文本或 JSON 定义，由大模型一键生成完整测验结构
- **AI 图片生成** — 封面图、结果形象图支持接入豆包等文生图接口
- **结果分享图** — 自动合成专属分享图，支持微信分享
- **历史记录** — 同一 Token 可查看历史答题记录与结果详情
- **数据统计** — 各测验参与人数、结果分布可视化
- **文件存储** — 图片统一存储于 MinIO，访问链接使用预签名 URL

## 技术栈

| 层        | 技术                                                                           |
|----------|------------------------------------------------------------------------------|
| 后端       | Python 3.12 · FastAPI · SQLAlchemy 2.0 · PostgreSQL · Redis · MinIO · Celery |
| 管理端（PC）  | Vue 3 · Vite · Naive UI · Tailwind CSS · TypeScript                          |
| 用户端（移动端） | Vue 3 · Vite · Vant · Tailwind CSS · TypeScript                              |

## 截图

### 管理端（PC）

**测验列表** — 测验管理主页，展示所有测验的名称、编码、类型、状态、题目数、结果数及参与人数，支持按状态/类型筛选和关键词搜索

![测验管理列表](doc/images/web/01.png)

**新建/编辑测验** — 弹窗快速编辑测验基本信息，包括名称、编码、类型、封面图（支持 AI 生成提示词）、分享标题与描述

![编辑测验信息](doc/images/web/02.png)

**测验详情 · 基本信息** — 测验详情页的基本信息 Tab，封面图旁显示 AI 文生图提示词，便于重新生成

![基本信息](doc/images/web/03.png)

**测验详情 · 题目配置** — 题目配置 Tab，支持题目图片、各选项图片、选项分值（score 类型）和隐藏判定题标记

![题目配置](doc/images/web/04.png)

**测验详情 · 结果配置** — 结果配置 Tab，展示并编辑每个结果的名称、形象图、摘要标签及详细解读

![结果配置](doc/images/web/05.png)

**测验详情 · 算法配置** — 算法配置 Tab，以累分映射为例展示分值范围和特殊判定规则（可设定隐藏触发条件直接命中特定结果）

![算法配置](doc/images/web/06.png)

**测验详情 · 数据统计** — 数据统计 Tab，显示 Token 总数、已使用数、核销率，以及各结果的命中人数分布条形图

![数据统计](doc/images/web/07.png)

**Token 管理列表** — Token 管理页，展示已生成 Token 的使用进度（已用/上限）、状态、批次编号、授权测验范围、来源和过期时间

![Token 列表](doc/images/web/08.png)

**Token 授权测验** — 为单个 Token 选择可访问的已发布测验，支持搜索和多选

![授权测验弹窗](doc/images/web/09.png)

---

### 用户端（移动端）

**入口页** — 用户凭链接进入后看到通行证状态（可用/已用次数/上限）、可参加的测验列表（含封面图和描述）、搜索框和历史记录入口

![移动端入口页](doc/images/mobile/01.png)

**测验介绍** — 选中测验后弹出介绍卡片，展示封面图、测验名称和题目总数，点击「开始测试」进入答题

![测验介绍弹窗](doc/images/mobile/02.png)

**答题页** — 题目页展示当前进度（1/11）、题目图片、题目内容和选项列表（选项支持配图），支持上一题/下一题导航

![答题页](doc/images/mobile/03.png)

**结果页** — 答题结束后即时展示人格类型名称、结果形象图、匹配度百分比及详细解读文案，底部提供关闭和分享按钮

![结果页](doc/images/mobile/04.png)

**历史记录** — 点击右上角「历史」弹出历史面板，列出该 Token 所有历史答题记录（测验名称、结果名称、匹配度），支持搜索和点击回看详情

![历史记录](doc/images/mobile/05.png)

## 项目结构

```
fun_quiz/
├── backend/          # FastAPI 后端
│   ├── app/          # 路由注册（*_router.py → /api/{模块名}）
│   ├── basic/        # 基础设施（BaseEntity / BaseRepository / UoW / MinIO / Redis）
│   ├── basic_module/ # 通用业务（用户 / 权限 / 角色 / 组织 / 文件存储）
│   ├── biz_module/   # 测验业务（Quiz / Token / 算法 / 统计）
│   └── config/       # 配置（.env + TOML，分 dev / test / prod）
├── web/              # 管理端前端（PC）
└── mobile/           # 用户端前端（移动端）
```

## 快速开始

### 环境要求

- Python 3.12+
- Node.js 18+ · Yarn
- PostgreSQL 14+
- Redis 6+
- MinIO

### 数据库初始化

```bash
# 将 SQL 文件中的 "dev" 替换为你的数据库用户名，然后执行
sed 's/dev/your_db_user/g' backend/doc/sql.sql | psql -U your_db_user -d your_db_name
```

也可以用编辑器打开 `backend/doc/sql.sql`，全局替换 `dev` 为实际用户名后再导入。

### 后端

```bash
cd backend

# 安装依赖
pip install poetry
poetry install

# 复制并填写环境变量（development / production 同理）
cp config/.env.development.example config/.env.development
# 编辑 DATABASE_URL / MINIO_* / REDIS_* 等变量

# 复制并填写应用配置（JWT / 端口等）
cp config/app_development_config.toml.example config/app_development_config.toml

# 启动
python run.py
```

主要环境变量（`config/.env.{env}`）：

```
DATABASE_URL=postgresql://user:pass@host:port/dbname
MINIO_ENDPOINT=host:port
MINIO_DEFAULT_BUCKET_NAME=fun-quiz
MINIO_DEFAULT_BUCKET_PATH=common
MINIO_ACCESS_KEY=...
MINIO_SECRET_KEY=...
MINIO_SECURE=false
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_PASSWORD=...
REDIS_DB=0
```

主要 TOML 配置项（`config/app_{env}_config.toml`）：

```toml
[storage]
max_file_size = 2048

[jwt]
REFRESH_TOKEN_EXPIRE_DAYS = 7
ACCESS_TOKEN_EXPIRE_MINUTES = 120
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
TOKEN_TYPE = "Bearer"

[fastapi]
port = 8403
```

### 管理端（PC）

```bash
cd web

# 复制并填写 API 地址
cp .env.development.example .env.development

yarn install
yarn dev
```

### 用户端（移动端）

```bash
cd mobile

# 复制并填写 API 地址
cp .env.development.example .env.development

yarn install
yarn dev
```

## AI 生成测验（Agent Skill）

本项目内置了一个 Agent Skill，可通过自然语言描述一键生成完整的测验定义 JSON，再由管理端「AI 导入」功能导入。

skill目录

```markdown
doc/skill/generate-quiz
```

用法

```
/generate-quiz <自然语言描述>
```

示例：

```
/generate-quiz 做一个类似 SBTI 的职场人格测试，15 维向量，25 种人格，30 道题，幽默风格
/generate-quiz 做一个「你是哪种咖啡」累分型测试，20 道题，6 种结果
/generate-quiz 做一个 MBTI 风格测试，4 个轴，16 种人格，40 道题
```

Skill 会将生成的 JSON 保存到 `doc/generated/<quiz_code>.json`，人工审核后在管理端点击「AI 导入」上传即可。详见 [
`doc/skill/generate-quiz/SKILL.md`](doc/skill/generate-quiz/SKILL.md)。

## 使用流程

1. **管理端**登录后，在「测验管理」中创建测验（手动或 AI 导入）
2. 配置题目、结果、算法参数，发布测验
3. 在「Token 管理」中批量生成访问令牌，设置可用次数和有效期
4. 将 `https://your-domain/entry?token=xxx` 形式的链接分发给用户
5. 用户打开链接，选择测验作答，即时查看结果，支持历史记录回溯

## 私有化部署等相关事宜

请联系

```markdown
268zhb@gmail.com
```

## License

[MIT](LICENSE)
