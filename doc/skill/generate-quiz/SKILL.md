# Quiz 生成 Skill 规范

管理员通过此 Skill 描述测验需求，AI 生成符合平台导入格式的完整测验定义 JSON，经人工审核后一键导入。

---

## 一、触发方式

在 Claude Code 中运行：

```
/generate-quiz <自然语言描述>
```

示例：
```
/generate-quiz 做一个类似SBTI的职场人格测试，15维向量，25种人格，30道题，幽默风格
/generate-quiz 做一个「你是哪种咖啡」累分型测试，20道题，6种结果
/generate-quiz 做一个MBTI风格测试，4个轴，16种人格，40道题
```

---

## 二、AI 输出格式（Quiz Definition JSON）

AI 必须严格输出以下结构的 JSON，保存为 `doc/generated/<quiz_code>.json`。

### 顶层结构

```json
{
  "meta": { ... },
  "algo_config": { ... },
  "special_rules": [ ... ],
  "questions": [ ... ],
  "outcomes": [ ... ]
}
```

---

### meta（映射 bt_quiz）

```json
{
  "meta": {
    "name": "职场人格测试",
    "code": "workplace_sbti",
    "quiz_type": "vector",
    "share_title": "你是哪种职场人？",
    "share_desc": "31道题揭开你的职场真面目",
    "fallback_outcome_code": "NORMAL",
    "cover_prompt": {
      "prompt": "一个 MBTI 人格形象的社畜双眼失焦瘫在格子间工位，咖啡杯倒了流一桌没人扶，屏幕弹「再改一版」气泡，头顶漂浮「班味+99」「KPI」「日报」字样，MBTI 插画风，chibi Q 版 2.5 头身，圆润线条，马卡龙粉纯色大色块背景，细黑描边",
      "style": "meme"
    },
    "result_config": {
      "bg_color": "#f5f5f5",
      "show_radar": true,
      "show_tags": true
    }
  }
}
```

`cover_prompt.prompt` 必须是中文，≤500字符，适配即梦（Dreamina）等中文文生图模型，MBTI 人格插画画风 × 恶趣味网络热梗内核（参考下方图片提示词规范）。

`quiz_type` 取值：`vector` | `score` | `branch` | `random`

---

### algo_config（按 quiz_type 变化）

**vector 类型**（多维向量匹配，如 SBTI/MBTI）：
```json
{
  "algo_config": {
    "similarity_threshold": 60,
    "dimensions": [
      { "code": "S1", "name": "自尊自信", "group_code": "S", "group_name": "自我模型", "sort_order": 1 },
      { "code": "S2", "name": "自我清晰度", "group_code": "S", "group_name": "自我模型", "sort_order": 2 }
    ]
  }
}
```

**score 类型**（累分段映射）：
```json
{
  "algo_config": {
    "total_min": 0,
    "total_max": 100
  }
}
```

**branch 类型**（分支跳题）：
```json
{
  "algo_config": {}
}
```

**random 类型**（加权随机）：
```json
{
  "algo_config": {}
}
```

---

### special_rules（映射 bt_quiz.special_rules）

```json
{
  "special_rules": [
    {
      "condition_type": "option_selected",
      "question_seq": 5,
      "option_key": "C",
      "trigger_outcome_code": "DRUNK_MASTER"
    }
  ]
}
```

`condition_type` 取值：`option_selected`（选了某选项）| `score_range`（总分在某区间）

---

### questions（映射 bt_quiz_question）

**vector 类型题目**：
```json
{
  "questions": [
    {
      "seq": 1,
      "content": "外人对我的评价来说无所吊谓。",
      "is_hidden": false,
      "image_prompt": {
        "prompt": "一个 MBTI 插画风的 i 人戴降噪耳机瘫坐在茶水间，周围同事叽叽喳喳围观吃瓜，他嘴角机械假笑眼神死鱼头顶气泡「关我屁事」，MBTI 人格插画风，chibi Q 版 2.5 头身，圆润线条，奶油黄纯色大色块背景，细黑描边",
        "style": "meme"
      },
      "options": [
        { "key": "A", "label": "不认同", "dim_scores": { "S1": 1 }, "image_prompt": { "prompt": "一只 MBTI 卡通形象的 chibi 小狗耷拉耳朵举着「被说中了」牌子脸红发烫气泡「嘴硬中…」，MBTI 人格插画风，圆润线条，马卡龙粉纯色大色块背景，细黑描边", "style": "meme" } },
        { "key": "B", "label": "中立",   "dim_scores": { "S1": 2 } },
        { "key": "C", "label": "认同",   "dim_scores": { "S1": 3 }, "image_prompt": { "prompt": "一个 MBTI 人格形象的爹系打工人戴墨镜昂首阔步，同事自动让路弯腰行注目礼头顶飘字「社会我哥」，MBTI 插画风，chibi 2.5 头身，圆润线条，薄荷绿纯色大色块背景，细黑描边", "style": "meme" } }
      ]
    }
  ]
}
```

`image_prompt` 为可选字段，**只在视觉表达能显著提升趣味性时生成**，否则留空（不要为每道题强制生成）。

**score 类型题目**：
```json
{
  "questions": [
    {
      "seq": 1,
      "content": "你会为喜欢的人主动付钱吗？",
      "is_hidden": false,
      "options": [
        { "key": "A", "label": "不会",   "score": 0 },
        { "key": "B", "label": "偶尔会", "score": 5 },
        { "key": "C", "label": "必须的", "score": 10 }
      ]
    }
  ]
}
```

**branch 类型题目**：
```json
{
  "questions": [
    {
      "seq": 1,
      "content": "你更喜欢哪种工作方式？",
      "is_hidden": false,
      "branch_config": { "default_next_seq": 2 },
      "options": [
        { "key": "A", "label": "独立完成", "next_question_seq": 2 },
        { "key": "B", "label": "团队协作", "next_question_seq": 5 },
        { "key": "C", "label": "看情况",   "next_question_seq": 3 }
      ]
    },
    {
      "seq": 10,
      "content": "（终止节点示例）",
      "is_hidden": false,
      "options": [
        { "key": "A", "label": "选项A", "next_question_seq": -1, "outcome_code": "TYPE_A" },
        { "key": "B", "label": "选项B", "next_question_seq": -1, "outcome_code": "TYPE_B" }
      ]
    }
  ]
}
```

**隐藏触发题**（所有类型通用）：
```json
{
  "seq": 8,
  "content": "（此题不展示维度，根据 special_rules 触发特殊结果）",
  "is_hidden": true,
  "options": [
    { "key": "A", "label": "不喝酒", "score": 0 },
    { "key": "B", "label": "偶尔喝", "score": 1 },
    { "key": "C", "label": "顿顿喝", "score": 2 }
  ]
}
```

---

### outcomes（映射 bt_quiz_outcome）

**vector 类型结果**：
```json
{
  "outcomes": [
    {
      "code": "ATM-er",
      "name": "送钱者",
      "summary": "恭喜你，你是稀有物种。",
      "detail": "你天生慷慨，把钱给出去的速度比ATM还快...",
      "tags": ["高付出", "社交边界低", "情感依赖"],
      "is_fallback": false,
      "is_special": false,
      "avatar_prompt": {
        "prompt": "一台 MBTI 人格形象化的 ATM 机长出细腿和颤抖小手嘴角抽搐强撑假笑，钞票哗哗往外喷眼角挂一滴泪，胸前挂「随取随取不限次」木牌，MBTI 插画风，chibi Q 版 2.5 头身，圆润线条，藕粉纯色大色块背景，细黑描边",
        "style": "meme"
      },
      "match_config": {
        "dim_vector": [3, 3, 2, 3, 2, 1, 3, 2, 1, 3, 2, 1, 1, 2, 1]
      }
    }
  ]
}
```

**score 类型结果**：
```json
{
  "outcomes": [
    {
      "code": "HEAVY_LOVER",
      "name": "重度恋爱脑",
      "summary": "你的爱情浓度超标了",
      "detail": "...",
      "tags": ["为爱冲动", "感性优先"],
      "is_fallback": false,
      "is_special": false,
      "match_config": { "score_min": 80, "score_max": 100 }
    }
  ]
}
```

**random 类型结果**：
```json
{
  "outcomes": [
    {
      "code": "LATTE",
      "name": "拿铁",
      "summary": "温柔而有品味",
      "detail": "...",
      "is_fallback": false,
      "is_special": false,
      "match_config": { "weight": 15 }
    }
  ]
}
```

**兜底结果**（is_fallback: true，每个测验至少一个）：
```json
{
  "code": "NORMAL",
  "name": "普通人",
  "is_fallback": true,
  "is_special": false,
  "match_config": {}
}
```

**特殊触发结果**（is_special: true，由 special_rules 命中）：
```json
{
  "code": "DRUNK_MASTER",
  "name": "酒神",
  "is_fallback": false,
  "is_special": true,
  "match_config": {}
}
```

---

## 三、AI 生成约束

生成时必须遵守以下规则：

1. **维度覆盖**（vector 类型）：每个维度必须至少被 2 道题覆盖；`dim_scores` 值只能是 1/2/3
2. **兜底结果**：每个测验必须有且只有一个 `is_fallback: true` 的结果，其 code 与 `meta.fallback_outcome_code` 一致
3. **向量长度**（vector 类型）：`dim_vector` 长度必须等于 `algo_config.dimensions` 的数量
4. **分值连续**（score 类型）：所有 outcomes 的 `score_min/score_max` 必须完整覆盖 `algo_config.total_min` 到 `total_max`，无缝隙无重叠
5. **branch 终止**（branch 类型）：所有路径必须能到达 `next_question_seq: -1` 的终止节点
6. **文案风格统一**：所有 outcome 的 detail 文案风格必须一致（由用户在 prompt 中指定）
7. **code 唯一**：同一测验内 outcome code 不得重复；question seq 不得重复
8. **JSON 合法性**：输出必须是合法的 JSON。所有字符串中禁止出现未转义的英文双引号 `"`，改用中文引号 `「」` 或 `『』`；禁止在字符串中直接换行，需用 `\n`；生成完毕后必须在心里过一遍 JSON.parse，确保可以被正确解析后再写入文件

---

## 四、文案风格规范（恶趣味）

所有题目、选项、结果文案默认采用「有点坏、有点准、让人又好气又好笑」的恶趣味风格，具体要求：

- **题目**：日常场景切入，藏着对人性的精准吐槽，让答题者心虚又忍不住选
  - ✅ 「周一早上闹钟响了，你的第一反应是？」
  - ✅ 「朋友发来60秒语音，你会？」
  - ❌ 「你如何处理工作压力？」（太正经）
- **选项**：不写正确答案，只写真实反应。A 选项永远是那个「没人承认但人人都做过」的选择
  - ✅ A「假装没看见，明天再说」B「硬着头皮听完」C「1.5倍速+中途划走」
  - ❌ A「积极回复」B「认真倾听」（假的）
- **outcome summary**：一句话精准戳穿人设，像被人当场抓包
  - ✅ 「你的人设是淡泊名利，实际上是懒得争」
  - ✅ 「表面随缘，内心OS已经把对方骂了三遍」
- **outcome detail**：200-400字，口吻像一个知道你所有秘密的老朋友在当面数落你，但又带着某种理解和包容。可以有夸张比喻、生活化类比，结尾给一个「歪打正着的人生建议」
  - ✅ 结尾：「建议你把『随便』这两个字纹在手上，省得每次都要说。」
  - ✅ 结尾：「好消息是，你这种人很难被PUA；坏消息是，你自己就是自己的PUA。」

---

## 五、导入方式

生成的 JSON 文件保存到 `doc/generated/<quiz_code>.json`，通过管理端「导入测验」功能上传，后端解析并写入数据库。

---

## 六、图片提示词风格规范（即梦适配 · MBTI 插画画风 × 恶趣味梗图内核）

所有 `image_prompt.prompt` 字段必须满足以下要求：

### 1. 硬约束

- **纯中文**，优先适配即梦（Dreamina），兼容可灵、通义万象、Midjourney 中文等
- **≤500 字符**
- **JSON 合法**：不出现英文双引号（用「」代替），不出现真实换行（用 `\n`）

### 2. 核心定位（必读）

**视觉画风 = MBTI 人格形象插画风**

- 参考小红书 / 抖音 / 微博上刷到的 MBTI 16 型人格卡通形象：扁平矢量、chibi Q 版 2.5 头身、圆润线条或细黑描边、角色居中、纯色大色块背景（马卡龙粉 / 奶油黄 / 薄荷绿 / 藕粉 / 浅紫 / 浅蓝 等），画面干净治愈有记忆点
- 不走粗糙表情包 / 魔性涂鸦路线，走「人格形象卡」的精致治愈感
- 角色必须身份化：身份词 + 专属小配件（工牌 / 奶茶 / 皇冠 / 充电宝 / 快递山 等），一眼可识别

**内容内核 = 恶趣味网络热梗**

- 身份 / 动作 / 表情 / 字幕 / 小道具必须精准戳中一个当下的梗或人性弱点（牛马 / 班味 / i 人社死 / 恋爱脑 / 发疯文学 / 孔乙己的长衫 / 脆皮青年 等）
- 画风越治愈，反差越好笑

**一句话记住：MBTI 的皮 · 恶趣味的魂。**

### 3. 即梦友好的结构化写法

推荐按顺序组织（越靠前权重越大）：

```
【身份词+MBTI 角色形象】+【动作/表情/情绪】+【梗点道具·字幕气泡】+【MBTI 插画画风锚定】+【纯色大色块背景与配色】
```

**拆解示例：**

```
一只 MBTI 人格形象的牛马打工人（身份 + MBTI 形象）
脖挂工牌瘫在工位眼神死鱼（动作/表情）
屏幕弹「再改一版」气泡，头顶漂浮「班味+99」（梗点道具 + 字幕）
MBTI 人格插画风，chibi Q 版 2.5 头身，圆润线条（画风锚定）
马卡龙粉纯色大色块背景，细黑描边（色彩构图）
```

### 4. 素材库（优先调用，越具体越戳人）

**网络热梗身份词**：打工人 / 牛马 / 班味 / 脆皮年轻人 / 孔乙己的长衫 / 摆烂 / 躺平 / 发疯文学 / 精神状态良好 / 已读乱回 / 一眼丁真 / 鉴定为 / 典中典 / 啊对对对 / 家人们谁懂啊 / 显眼包 / 纯爱战神 / 恋爱脑 / CPU 烧了 / i 人社死 / e 人狂喜 / 人机 / 红温 / 破防 / 爹系 / 妈系 / 纯欲 / 清冷 / 淡人 / 浓人 / 早 C 晚 A

**姿态 / 表情**：葛优躺 / 机械假笑 / 眼神死鱼 / 嘴角抽搐 / 翻白眼 / 内心 OS 气泡 / 双手合十装圣母 / 拿放大镜鉴定 / 捂脸大哭 / 皇冠掉一地 / 赛博上香 / 瘫成一滩 / 红温脸蛋

**场景道具**：格子间工位 / 打卡机 / 外卖袋 / 冰美式 / KPI 报表 / 已读不回手机屏 / 「年度最佳员工」奖杯（反讽）/ 省略号气泡 / 泡面桶里插奖状 / 满地订单号 / 未读消息爆炸 / 工牌 / 充电宝 / 小金皇冠

**画面风格词（默认首选 MBTI 插画画风，不走粗糙表情包路线）**：
MBTI 人格插画风 / MBTI 性格形象卡通 / MBTI 16 型人格插画 / 扁平矢量插画 / chibi Q 版 2.5 头身 / 大头可爱比例 / 圆润线条 / 极简构图 / 治愈系卡通 / 角色形象卡 / 人物居中半身或全身像

**色彩词（默认纯色大色块背景，马卡龙 / 奶油调）**：
马卡龙粉 / 奶油黄 / 薄荷绿 / 藕粉 / 浅紫 / 浅蓝 纯色大色块背景 / 细黑描边或无描边 / 柔和平涂色块 / 干净治愈配色

### 5. 写作要点（一针见血的核心）

- **身份 + MBTI 形象连写**：「一只 MBTI 人格形象的牛马打工人」「一位 MBTI 插画风的纯爱战神」「一个 MBTI 卡通形象的发疯学家」—— 身份词和画风锚点同时出现效果最佳
- **梗点前置**：最戳人的细节（身份、动作、字幕）放前半段，即梦会更忠实地抓取
- **画面写字**：把要出现的中文短句直接写进 prompt，如「关我屁事」「班味+99」「被说中了」「CPU 烧了」—— 即梦能较稳定输出中文短字
- **反差 / 矛盾**：治愈画风配崩溃灵魂、嘴笑内心骂街、西装革履配拖鞋、皇冠掉落、奖杯插泡面
- **避免空泛**：不要"在工作 / 在思考 / 在生活"，要"卡在哪一秒被戳中"
- **禁用中英混杂 / 摄影术语**（cinematic / bokeh / DSLR 等），偏离 MBTI 插画调性
- **禁用粗糙表情包路线**：不把"抽象涂鸦 / 魔性漫画 / 表情包美学 / 白底粗描边"作主画风锚点，改用 MBTI 插画风系列锚点
- **只在梗点强时配图**，没好梗就留空

### 6. 对照示例

- ✅ 「一只 MBTI 人格形象的牛马打工人脖挂工牌瘫在工位眼神死鱼，屏幕弹「再改一版」气泡，头顶漂浮「班味+99」，MBTI 插画风，chibi Q 版 2.5 头身，圆润线条，马卡龙粉纯色大色块背景，细黑描边」
- ✅ 「一个 MBTI 插画风的 i 人捧奶茶站在聚会角落机械假笑嘴角抽搐，头顶气泡「哈哈哈下次一定」脚边小字「社交电量 1%」，扁平矢量卡通，chibi 2.5 头身，奶油黄纯色背景，治愈系卡通」
- ✅ 「一位 MBTI 性格形象卡通的纯爱战神少女跪地双手奉上手机充电宝眼冒粉红爱心，头顶飘字「纯爱战神」胸口弹幕「CPU 烧了」，MBTI 人格插画风，圆润线条，薄荷绿纯色大色块背景，细黑描边」
- ✅ 「一个 MBTI 人格插画形象的孔乙己长衫青年蹲在共享单车旁啃冰美式外卖，脚边散着「985」「硕士」文凭牌，腰间小字「脆皮状态 100%」，扁平矢量治愈卡通，chibi 2.5 头身，藕粉纯色背景」
- ❌ 「一个人在工作」（太平淡，没身份没梗没画风）
- ❌ 「精美写实，电影级光影，cinematic」（偏离 MBTI 插画，且即梦梗图风用不上摄影术语）
- ❌ 「一个 sad 的 office worker」（中英混杂）
- ❌ 「扁平梗图插画，表情包美学，白底粗描边，抽象魔性漫画」（走粗糙表情包路线，偏离 MBTI 人格插画的精致治愈感）

---

## 七、Skill 提示词模板

```
你是一个专门设计恶趣味测验的设计师，擅长用「有点坏、有点准、让人又好气又好笑」的风格戳穿人性。

需求：{{user_description}}

严格遵守 SKILL.md 中定义的输出格式、文案风格规范和图片提示词规范，生成完整测验定义 JSON。

图片提示词要求（适配即梦 Dreamina · MBTI 插画画风 × 恶趣味网络热梗内核）：
- 核心定位：**MBTI 的皮 · 恶趣味的魂**——视觉走 MBTI 16 型人格卡通形象那种扁平矢量治愈插画，内容走戳心一针见血的网络热梗
- 纯中文，≤500 字符，不要中英混杂，不要摄影术语（cinematic / bokeh / DSLR 等）
- 结构：【身份词+MBTI 角色形象】+【动作/表情】+【梗点道具·字幕气泡】+【MBTI 插画画风锚定】+【纯色大色块背景与配色】
- 身份 + 画风连写：「一只 MBTI 人格形象的牛马打工人」「一位 MBTI 插画风的纯爱战神」「一个 MBTI 卡通形象的发疯学家」等
- 画面直接写中文短句（「关我屁事」「班味+99」「被说中了」「CPU 烧了」等），即梦能较稳定出中文短字
- 反差 / 精准踩雷：治愈画风 × 崩溃灵魂、嘴笑 OS 骂街、皇冠掉落、奖杯插泡面
- 默认画风锚定词：MBTI 人格插画风 / 扁平矢量 / chibi Q 版 2.5 头身 / 圆润线条 / 细黑描边或无描边 / 治愈系卡通
- 默认配色锚定词：马卡龙粉 / 奶油黄 / 薄荷绿 / 藕粉 / 浅紫 / 浅蓝 纯色大色块背景，柔和平涂
- 禁用项：粗糙表情包 / 魔性涂鸦 / 白底粗描边 / 抽象梗图 这类锚点（偏离 MBTI 人格插画的精致治愈感）
- meta.cover_prompt 必须生成，梗点要硬且画风统一
- 每个 outcome 必须生成 avatar_prompt，做成「MBTI 人格形象卡」风格，一眼戳中该类型的精神状态
- 题目 / 选项的 image_prompt 选择性生成，没想到强梗就留空；选项 image_prompt 写在选项对象的 image_prompt 字段

JSON 合法性要求（必须遵守）：
- 所有字符串内禁止出现未转义的英文双引号，改用「」
- 字符串内换行用 \n 表示
- 生成完毕后检查 JSON 结构是否合法，再保存到 doc/generated/{{quiz_code}}.json

生成完毕后简要说明：测验类型、题目数、结果数、核心算法思路。
```
