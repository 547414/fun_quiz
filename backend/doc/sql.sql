/*
 Navicat Premium Dump SQL

 Source Server         : fun_quiz_dev
 Source Server Type    : PostgreSQL
 Source Server Version : 160013 (160013)
 Source Host           : localhost:5458
 Source Catalog        : fun_quiz_dev
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 160013 (160013)
 File Encoding         : 65001

 Date: 22/04/2026 16:37:32
*/


-- ----------------------------
-- Type structure for enumpermissionassigngranteetype
-- ----------------------------
DROP TYPE IF EXISTS "public"."enumpermissionassigngranteetype";
CREATE TYPE "public"."enumpermissionassigngranteetype" AS ENUM (
  'ROLE',
  'USER',
  'WECOM_USER'
);
ALTER TYPE "public"."enumpermissionassigngranteetype" OWNER TO "dev";

-- ----------------------------
-- Type structure for enumpermissionassigngranttype
-- ----------------------------
DROP TYPE IF EXISTS "public"."enumpermissionassigngranttype";
CREATE TYPE "public"."enumpermissionassigngranttype" AS ENUM (
  'MENU',
  'BACKEND_API'
);
ALTER TYPE "public"."enumpermissionassigngranttype" OWNER TO "dev";

-- ----------------------------
-- Type structure for enumpermissionassignpolicy
-- ----------------------------
DROP TYPE IF EXISTS "public"."enumpermissionassignpolicy";
CREATE TYPE "public"."enumpermissionassignpolicy" AS ENUM (
  'ALLOW',
  'DENY'
);
ALTER TYPE "public"."enumpermissionassignpolicy" OWNER TO "dev";

-- ----------------------------
-- Type structure for enumresourcepermissioncategory
-- ----------------------------
DROP TYPE IF EXISTS "public"."enumresourcepermissioncategory";
CREATE TYPE "public"."enumresourcepermissioncategory" AS ENUM (
  'MENU',
  'BACKEND_API'
);
ALTER TYPE "public"."enumresourcepermissioncategory" OWNER TO "dev";

-- ----------------------------
-- Table structure for bt_quiz
-- ----------------------------
DROP TABLE IF EXISTS "public"."bt_quiz";
CREATE TABLE "public"."bt_quiz" (
  "name" varchar(200) COLLATE "pg_catalog"."default" NOT NULL,
  "code" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "covers" jsonb,
  "cover_prompt" jsonb,
  "quiz_type" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'vector'::character varying,
  "status" varchar(20) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'draft'::character varying,
  "source" varchar(20) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'manual'::character varying,
  "sort_order" int4 NOT NULL DEFAULT 0,
  "share_title" varchar(200) COLLATE "pg_catalog"."default",
  "share_desc" varchar(500) COLLATE "pg_catalog"."default",
  "fallback_outcome_code" varchar(100) COLLATE "pg_catalog"."default",
  "algo_config" jsonb,
  "special_rules" jsonb,
  "result_config" jsonb,
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."bt_quiz" OWNER TO "dev";
COMMENT ON COLUMN "public"."bt_quiz"."name" IS '测验名称';
COMMENT ON COLUMN "public"."bt_quiz"."code" IS '测验编码，唯一标识';
COMMENT ON COLUMN "public"."bt_quiz"."covers" IS '封面图文件列表 JSON Array';
COMMENT ON COLUMN "public"."bt_quiz"."cover_prompt" IS '封面图生成提示词配置 JSON';
COMMENT ON COLUMN "public"."bt_quiz"."quiz_type" IS '测验类型';
COMMENT ON COLUMN "public"."bt_quiz"."status" IS '状态：draft/published/archived';
COMMENT ON COLUMN "public"."bt_quiz"."source" IS '创建来源：manual/ai';
COMMENT ON COLUMN "public"."bt_quiz"."sort_order" IS '排序';
COMMENT ON COLUMN "public"."bt_quiz"."share_title" IS '分享标题';
COMMENT ON COLUMN "public"."bt_quiz"."share_desc" IS '分享描述';
COMMENT ON COLUMN "public"."bt_quiz"."fallback_outcome_code" IS '兜底结果编码（匹配度不足时使用）';
COMMENT ON COLUMN "public"."bt_quiz"."algo_config" IS '算法配置 JSON，结构随 quiz_type 变化（详见 doc/SKILL.md）';
COMMENT ON COLUMN "public"."bt_quiz"."special_rules" IS '特殊判定规则 JSON（详见 doc/SKILL.md）';
COMMENT ON COLUMN "public"."bt_quiz"."result_config" IS '结果页展示配置 JSON（详见 doc/SKILL.md）';
COMMENT ON COLUMN "public"."bt_quiz"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."bt_quiz"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."bt_quiz"."operator" IS '操作者';
COMMENT ON COLUMN "public"."bt_quiz"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."bt_quiz"."version" IS '版本号';
COMMENT ON COLUMN "public"."bt_quiz"."desc" IS '描述';
COMMENT ON TABLE "public"."bt_quiz" IS '测验主表';

-- ----------------------------
-- Records of bt_quiz
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for bt_quiz_outcome
-- ----------------------------
DROP TABLE IF EXISTS "public"."bt_quiz_outcome";
CREATE TABLE "public"."bt_quiz_outcome" (
  "quiz_id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL,
  "code" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "name" varchar(200) COLLATE "pg_catalog"."default" NOT NULL,
  "avatar" jsonb,
  "avatar_prompt" jsonb,
  "summary" varchar(500) COLLATE "pg_catalog"."default",
  "detail" varchar COLLATE "pg_catalog"."default",
  "tags" jsonb,
  "sort_order" int4 NOT NULL DEFAULT 0,
  "is_fallback" bool NOT NULL DEFAULT false,
  "is_special" bool NOT NULL DEFAULT false,
  "match_config" jsonb,
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."bt_quiz_outcome" OWNER TO "dev";
COMMENT ON COLUMN "public"."bt_quiz_outcome"."quiz_id" IS '所属测验ID';
COMMENT ON COLUMN "public"."bt_quiz_outcome"."code" IS '结果编码，同一测验内唯一，如 ATM-er / INTJ / LATTE';
COMMENT ON COLUMN "public"."bt_quiz_outcome"."name" IS '结果名称';
COMMENT ON COLUMN "public"."bt_quiz_outcome"."avatar" IS '结果形象图文件 JSON';
COMMENT ON COLUMN "public"."bt_quiz_outcome"."avatar_prompt" IS '结果头像生成提示词配置 JSON';
COMMENT ON COLUMN "public"."bt_quiz_outcome"."summary" IS '结果简短描述（结果页副标题）';
COMMENT ON COLUMN "public"."bt_quiz_outcome"."detail" IS '结果详细解读文案（支持富文本）';
COMMENT ON COLUMN "public"."bt_quiz_outcome"."tags" IS '特征标签 JSON，如 ["高付出","社交边界低"]';
COMMENT ON COLUMN "public"."bt_quiz_outcome"."sort_order" IS '排序';
COMMENT ON COLUMN "public"."bt_quiz_outcome"."is_fallback" IS '是否为兜底结果';
COMMENT ON COLUMN "public"."bt_quiz_outcome"."is_special" IS '是否为特殊触发结果（由 special_rules 命中）';
COMMENT ON COLUMN "public"."bt_quiz_outcome"."match_config" IS '匹配条件 JSON，结构随 quiz_type 变化';
COMMENT ON COLUMN "public"."bt_quiz_outcome"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."bt_quiz_outcome"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."bt_quiz_outcome"."operator" IS '操作者';
COMMENT ON COLUMN "public"."bt_quiz_outcome"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."bt_quiz_outcome"."version" IS '版本号';
COMMENT ON COLUMN "public"."bt_quiz_outcome"."desc" IS '描述';
COMMENT ON TABLE "public"."bt_quiz_outcome" IS '测验结果模板表';

-- ----------------------------
-- Records of bt_quiz_outcome
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for bt_quiz_question
-- ----------------------------
DROP TABLE IF EXISTS "public"."bt_quiz_question";
CREATE TABLE "public"."bt_quiz_question" (
  "quiz_id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL,
  "seq" int4 NOT NULL,
  "content" varchar(1000) COLLATE "pg_catalog"."default" NOT NULL,
  "images" jsonb,
  "image_prompt" jsonb,
  "is_hidden" bool NOT NULL DEFAULT false,
  "options" jsonb NOT NULL,
  "branch_config" jsonb,
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."bt_quiz_question" OWNER TO "dev";
COMMENT ON COLUMN "public"."bt_quiz_question"."quiz_id" IS '所属测验ID';
COMMENT ON COLUMN "public"."bt_quiz_question"."seq" IS '题目序号，从1开始，branch类型用于跳转引用';
COMMENT ON COLUMN "public"."bt_quiz_question"."content" IS '题目内容';
COMMENT ON COLUMN "public"."bt_quiz_question"."images" IS '题目配图文件列表 JSON Array';
COMMENT ON COLUMN "public"."bt_quiz_question"."image_prompt" IS '题目图片生成提示词配置 JSON';
COMMENT ON COLUMN "public"."bt_quiz_question"."is_hidden" IS '是否隐藏判定题（配合 special_rules 触发特殊结果）';
COMMENT ON COLUMN "public"."bt_quiz_question"."options" IS '选项配置 JSON，结构随 quiz_type 变化';
COMMENT ON COLUMN "public"."bt_quiz_question"."branch_config" IS '分支跳题配置 JSON，仅 branch 类型使用';
COMMENT ON COLUMN "public"."bt_quiz_question"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."bt_quiz_question"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."bt_quiz_question"."operator" IS '操作者';
COMMENT ON COLUMN "public"."bt_quiz_question"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."bt_quiz_question"."version" IS '版本号';
COMMENT ON COLUMN "public"."bt_quiz_question"."desc" IS '描述';
COMMENT ON TABLE "public"."bt_quiz_question" IS '测验题目表';

-- ----------------------------
-- Records of bt_quiz_question
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for bt_quiz_result
-- ----------------------------
DROP TABLE IF EXISTS "public"."bt_quiz_result";
CREATE TABLE "public"."bt_quiz_result" (
  "token_id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL,
  "quiz_id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL,
  "answers" jsonb NOT NULL,
  "calc_result" jsonb,
  "outcome_code" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "outcome_id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL,
  "score" int4,
  "share_image" jsonb,
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."bt_quiz_result" OWNER TO "dev";
COMMENT ON COLUMN "public"."bt_quiz_result"."token_id" IS '关联的访问令牌ID（唯一，一个token只能产生一条结果）';
COMMENT ON COLUMN "public"."bt_quiz_result"."quiz_id" IS '所属测验ID';
COMMENT ON COLUMN "public"."bt_quiz_result"."answers" IS '原始答案 JSON，格式：{question_seq: option_key}';
COMMENT ON COLUMN "public"."bt_quiz_result"."calc_result" IS '计算中间结果 JSON，结构随 quiz_type 变化';
COMMENT ON COLUMN "public"."bt_quiz_result"."outcome_code" IS '命中结果编码';
COMMENT ON COLUMN "public"."bt_quiz_result"."outcome_id" IS '命中结果ID';
COMMENT ON COLUMN "public"."bt_quiz_result"."score" IS '匹配度（百分比），vector/score类型有值，其他为NULL';
COMMENT ON COLUMN "public"."bt_quiz_result"."share_image" IS '分享图文件 JSON';
COMMENT ON COLUMN "public"."bt_quiz_result"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."bt_quiz_result"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."bt_quiz_result"."operator" IS '操作者';
COMMENT ON COLUMN "public"."bt_quiz_result"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."bt_quiz_result"."version" IS '版本号';
COMMENT ON COLUMN "public"."bt_quiz_result"."desc" IS '描述';
COMMENT ON TABLE "public"."bt_quiz_result" IS '用户答题结果记录表';

-- ----------------------------
-- Records of bt_quiz_result
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for bt_quiz_token
-- ----------------------------
DROP TABLE IF EXISTS "public"."bt_quiz_token";
CREATE TABLE "public"."bt_quiz_token" (
  "token" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "status" varchar(20) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'active'::character varying,
  "max_uses" int4,
  "used_count" int4 NOT NULL DEFAULT 0,
  "source" varchar(20) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'admin'::character varying,
  "batch_code" varchar(100) COLLATE "pg_catalog"."default",
  "expires_at" timestamptz(6),
  "extra" jsonb,
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."bt_quiz_token" OWNER TO "dev";
COMMENT ON COLUMN "public"."bt_quiz_token"."token" IS '访问令牌（随机字符串），用于链接中的唯一标识';
COMMENT ON COLUMN "public"."bt_quiz_token"."status" IS '状态：active/exhausted/expired';
COMMENT ON COLUMN "public"."bt_quiz_token"."max_uses" IS '最大使用次数，NULL表示不限次数';
COMMENT ON COLUMN "public"."bt_quiz_token"."used_count" IS '已使用次数';
COMMENT ON COLUMN "public"."bt_quiz_token"."source" IS '令牌来源：purchase/gift/admin/batch';
COMMENT ON COLUMN "public"."bt_quiz_token"."batch_code" IS '批次编码，批量生成时使用，便于管理';
COMMENT ON COLUMN "public"."bt_quiz_token"."expires_at" IS '过期时间，NULL表示永不过期';
COMMENT ON COLUMN "public"."bt_quiz_token"."extra" IS '扩展信息 JSON，如购买订单号、赠送备注等';
COMMENT ON COLUMN "public"."bt_quiz_token"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."bt_quiz_token"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."bt_quiz_token"."operator" IS '操作者';
COMMENT ON COLUMN "public"."bt_quiz_token"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."bt_quiz_token"."version" IS '版本号';
COMMENT ON COLUMN "public"."bt_quiz_token"."desc" IS '描述';
COMMENT ON TABLE "public"."bt_quiz_token" IS '测验访问令牌表';

-- ----------------------------
-- Records of bt_quiz_token
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for bt_quiz_token_log
-- ----------------------------
DROP TABLE IF EXISTS "public"."bt_quiz_token_log";
CREATE TABLE "public"."bt_quiz_token_log" (
  "token_id" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "token_value" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "quiz_id" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "result_id" varchar(64) COLLATE "pg_catalog"."default",
  "outcome_code" varchar(100) COLLATE "pg_catalog"."default",
  "outcome_name" varchar(200) COLLATE "pg_catalog"."default",
  "ip" varchar(64) COLLATE "pg_catalog"."default",
  "user_agent" varchar(500) COLLATE "pg_catalog"."default",
  "used_count" int4 NOT NULL DEFAULT 0,
  "max_uses" int4,
  "batch_code" varchar(100) COLLATE "pg_catalog"."default",
  "source" varchar(20) COLLATE "pg_catalog"."default",
  "extra" jsonb,
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."bt_quiz_token_log" OWNER TO "dev";
COMMENT ON COLUMN "public"."bt_quiz_token_log"."token_id" IS '关联 bt_quiz_token.id';
COMMENT ON COLUMN "public"."bt_quiz_token_log"."token_value" IS 'token 明文，冗余便于展示';
COMMENT ON COLUMN "public"."bt_quiz_token_log"."quiz_id" IS '关联 bt_quiz.id';
COMMENT ON COLUMN "public"."bt_quiz_token_log"."result_id" IS '关联 bt_quiz_result.id';
COMMENT ON COLUMN "public"."bt_quiz_token_log"."outcome_code" IS '命中结果编码';
COMMENT ON COLUMN "public"."bt_quiz_token_log"."outcome_name" IS '命中结果名称';
COMMENT ON COLUMN "public"."bt_quiz_token_log"."ip" IS '客户端 IP';
COMMENT ON COLUMN "public"."bt_quiz_token_log"."user_agent" IS '客户端 User-Agent';
COMMENT ON COLUMN "public"."bt_quiz_token_log"."used_count" IS '本次消耗后已使用次数';
COMMENT ON COLUMN "public"."bt_quiz_token_log"."max_uses" IS 'token 最大使用次数，NULL 表示不限';
COMMENT ON COLUMN "public"."bt_quiz_token_log"."batch_code" IS 'token 批次编码（冗余）';
COMMENT ON COLUMN "public"."bt_quiz_token_log"."source" IS 'token 来源（冗余）';
COMMENT ON COLUMN "public"."bt_quiz_token_log"."extra" IS '扩展信息 JSON';
COMMENT ON COLUMN "public"."bt_quiz_token_log"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."bt_quiz_token_log"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."bt_quiz_token_log"."operator" IS '操作者';
COMMENT ON COLUMN "public"."bt_quiz_token_log"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."bt_quiz_token_log"."version" IS '版本号';
COMMENT ON COLUMN "public"."bt_quiz_token_log"."desc" IS '描述';
COMMENT ON TABLE "public"."bt_quiz_token_log" IS 'Token 消耗日志表';

-- ----------------------------
-- Records of bt_quiz_token_log
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for bt_quiz_token_quiz
-- ----------------------------
DROP TABLE IF EXISTS "public"."bt_quiz_token_quiz";
CREATE TABLE "public"."bt_quiz_token_quiz" (
  "token_id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL,
  "quiz_id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL,
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."bt_quiz_token_quiz" OWNER TO "dev";
COMMENT ON COLUMN "public"."bt_quiz_token_quiz"."token_id" IS '关联的 token ID';
COMMENT ON COLUMN "public"."bt_quiz_token_quiz"."quiz_id" IS '授权的测验 ID';
COMMENT ON COLUMN "public"."bt_quiz_token_quiz"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."bt_quiz_token_quiz"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."bt_quiz_token_quiz"."operator" IS '操作者';
COMMENT ON COLUMN "public"."bt_quiz_token_quiz"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."bt_quiz_token_quiz"."version" IS '版本号';
COMMENT ON COLUMN "public"."bt_quiz_token_quiz"."desc" IS '描述';
COMMENT ON TABLE "public"."bt_quiz_token_quiz" IS 'Token 授权测验关联表';

-- ----------------------------
-- Records of bt_quiz_token_quiz
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for ct_backend_api
-- ----------------------------
DROP TABLE IF EXISTS "public"."ct_backend_api";
CREATE TABLE "public"."ct_backend_api" (
  "name" varchar(500) COLLATE "pg_catalog"."default",
  "code" varchar(500) COLLATE "pg_catalog"."default",
  "enabled" bool NOT NULL DEFAULT true,
  "url" varchar(500) COLLATE "pg_catalog"."default" NOT NULL,
  "ignore_auth" bool NOT NULL DEFAULT false,
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."ct_backend_api" OWNER TO "dev";
COMMENT ON COLUMN "public"."ct_backend_api"."name" IS '名称';
COMMENT ON COLUMN "public"."ct_backend_api"."code" IS '编码';
COMMENT ON COLUMN "public"."ct_backend_api"."enabled" IS '是否启用';
COMMENT ON COLUMN "public"."ct_backend_api"."url" IS 'URL';
COMMENT ON COLUMN "public"."ct_backend_api"."ignore_auth" IS '是否忽略权限';
COMMENT ON COLUMN "public"."ct_backend_api"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."ct_backend_api"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."ct_backend_api"."operator" IS '操作者';
COMMENT ON COLUMN "public"."ct_backend_api"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."ct_backend_api"."version" IS '版本号';
COMMENT ON COLUMN "public"."ct_backend_api"."desc" IS '描述';
COMMENT ON TABLE "public"."ct_backend_api" IS '后端接口表';

-- ----------------------------
-- Records of ct_backend_api
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for ct_config_dict
-- ----------------------------
DROP TABLE IF EXISTS "public"."ct_config_dict";
CREATE TABLE "public"."ct_config_dict" (
  "name" varchar(255) COLLATE "pg_catalog"."default",
  "code" varchar(255) COLLATE "pg_catalog"."default",
  "data" jsonb,
  "enabled" bool NOT NULL DEFAULT true,
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."ct_config_dict" OWNER TO "dev";
COMMENT ON COLUMN "public"."ct_config_dict"."name" IS '名称';
COMMENT ON COLUMN "public"."ct_config_dict"."code" IS '编码';
COMMENT ON COLUMN "public"."ct_config_dict"."data" IS '配置数据';
COMMENT ON COLUMN "public"."ct_config_dict"."enabled" IS '是否启用';
COMMENT ON COLUMN "public"."ct_config_dict"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."ct_config_dict"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."ct_config_dict"."operator" IS '操作者';
COMMENT ON COLUMN "public"."ct_config_dict"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."ct_config_dict"."version" IS '版本号';
COMMENT ON COLUMN "public"."ct_config_dict"."desc" IS '描述';
COMMENT ON TABLE "public"."ct_config_dict" IS '配置字段表';

-- ----------------------------
-- Records of ct_config_dict
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for ct_dept
-- ----------------------------
DROP TABLE IF EXISTS "public"."ct_dept";
CREATE TABLE "public"."ct_dept" (
  "organization_id" varchar(40) COLLATE "pg_catalog"."default",
  "name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "code" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "category" varchar(255) COLLATE "pg_catalog"."default",
  "brief" text COLLATE "pg_catalog"."default",
  "parent_id" varchar(40) COLLATE "pg_catalog"."default",
  "source_category" varchar(255) COLLATE "pg_catalog"."default",
  "source_id" varchar(255) COLLATE "pg_catalog"."default",
  "seq" int4 NOT NULL,
  "enabled" bool NOT NULL,
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."ct_dept" OWNER TO "dev";
COMMENT ON COLUMN "public"."ct_dept"."organization_id" IS '组织ID';
COMMENT ON COLUMN "public"."ct_dept"."name" IS '部门名称';
COMMENT ON COLUMN "public"."ct_dept"."code" IS '部门编码';
COMMENT ON COLUMN "public"."ct_dept"."category" IS '部门类型';
COMMENT ON COLUMN "public"."ct_dept"."brief" IS '描述';
COMMENT ON COLUMN "public"."ct_dept"."parent_id" IS '父级部门ID';
COMMENT ON COLUMN "public"."ct_dept"."source_category" IS '来源类型，例如企微、钉钉等';
COMMENT ON COLUMN "public"."ct_dept"."source_id" IS '来源id';
COMMENT ON COLUMN "public"."ct_dept"."seq" IS '排序';
COMMENT ON COLUMN "public"."ct_dept"."enabled" IS '是否启用';
COMMENT ON COLUMN "public"."ct_dept"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."ct_dept"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."ct_dept"."operator" IS '操作者';
COMMENT ON COLUMN "public"."ct_dept"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."ct_dept"."version" IS '版本号';
COMMENT ON COLUMN "public"."ct_dept"."desc" IS '描述';
COMMENT ON TABLE "public"."ct_dept" IS '部门表';

-- ----------------------------
-- Records of ct_dept
-- ----------------------------
BEGIN;
INSERT INTO "public"."ct_dept" ("organization_id", "name", "code", "category", "brief", "parent_id", "source_category", "source_id", "seq", "enabled", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('421d02a8-a547-4568-8b04-2921d1a58b9a', '默认根部门', '000001', 'DEPARTMENT', NULL, NULL, NULL, NULL, 0, 't', '75f02c0d-f1ff-48c6-9c5a-d8bbcfc18141', '2026-01-15 16:11:16.537853+08', '2026-04-22 15:58:28.442901+08', 'b2e0bd5b-a1df-4391-8ba2-5ba5bbe0d3be', 'ROBOT', 2, NULL);
COMMIT;

-- ----------------------------
-- Table structure for ct_file_info
-- ----------------------------
DROP TABLE IF EXISTS "public"."ct_file_info";
CREATE TABLE "public"."ct_file_info" (
  "name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "file_storage_id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL,
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."ct_file_info" OWNER TO "dev";
COMMENT ON COLUMN "public"."ct_file_info"."name" IS '文件名';
COMMENT ON COLUMN "public"."ct_file_info"."file_storage_id" IS '文件存储ID';
COMMENT ON COLUMN "public"."ct_file_info"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."ct_file_info"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."ct_file_info"."operator" IS '操作者';
COMMENT ON COLUMN "public"."ct_file_info"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."ct_file_info"."version" IS '版本号';
COMMENT ON COLUMN "public"."ct_file_info"."desc" IS '描述';
COMMENT ON TABLE "public"."ct_file_info" IS '文件信息表';

-- ----------------------------
-- Records of ct_file_info
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for ct_file_resource
-- ----------------------------
DROP TABLE IF EXISTS "public"."ct_file_resource";
CREATE TABLE "public"."ct_file_resource" (
  "file_info_id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL,
  "resource_category" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "resource_id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL,
  "relationship" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."ct_file_resource" OWNER TO "dev";
COMMENT ON COLUMN "public"."ct_file_resource"."file_info_id" IS '文件信息ID';
COMMENT ON COLUMN "public"."ct_file_resource"."resource_category" IS '资源类型';
COMMENT ON COLUMN "public"."ct_file_resource"."resource_id" IS '资源ID';
COMMENT ON COLUMN "public"."ct_file_resource"."relationship" IS '关系';
COMMENT ON COLUMN "public"."ct_file_resource"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."ct_file_resource"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."ct_file_resource"."operator" IS '操作者';
COMMENT ON COLUMN "public"."ct_file_resource"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."ct_file_resource"."version" IS '版本号';
COMMENT ON COLUMN "public"."ct_file_resource"."desc" IS '描述';
COMMENT ON TABLE "public"."ct_file_resource" IS '文件资源关系表';

-- ----------------------------
-- Records of ct_file_resource
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for ct_file_storage
-- ----------------------------
DROP TABLE IF EXISTS "public"."ct_file_storage";
CREATE TABLE "public"."ct_file_storage" (
  "original_name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "object_name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "bucket_name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "path" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "endpoint" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "size" int4 NOT NULL,
  "type" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "hash" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."ct_file_storage" OWNER TO "dev";
COMMENT ON COLUMN "public"."ct_file_storage"."original_name" IS '原文件名';
COMMENT ON COLUMN "public"."ct_file_storage"."object_name" IS '对象名';
COMMENT ON COLUMN "public"."ct_file_storage"."bucket_name" IS '桶名';
COMMENT ON COLUMN "public"."ct_file_storage"."path" IS '路径';
COMMENT ON COLUMN "public"."ct_file_storage"."endpoint" IS '端点';
COMMENT ON COLUMN "public"."ct_file_storage"."size" IS '文件大小';
COMMENT ON COLUMN "public"."ct_file_storage"."type" IS '文件类型';
COMMENT ON COLUMN "public"."ct_file_storage"."hash" IS '文件哈希';
COMMENT ON COLUMN "public"."ct_file_storage"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."ct_file_storage"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."ct_file_storage"."operator" IS '操作者';
COMMENT ON COLUMN "public"."ct_file_storage"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."ct_file_storage"."version" IS '版本号';
COMMENT ON COLUMN "public"."ct_file_storage"."desc" IS '描述';
COMMENT ON TABLE "public"."ct_file_storage" IS '文件存储表';

-- ----------------------------
-- Records of ct_file_storage
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for ct_invite_code
-- ----------------------------
DROP TABLE IF EXISTS "public"."ct_invite_code";
CREATE TABLE "public"."ct_invite_code" (
  "code" varchar(500) COLLATE "pg_catalog"."default",
  "brief" text COLLATE "pg_catalog"."default",
  "max_limit" int4 NOT NULL DEFAULT 20,
  "register_num" int4 NOT NULL DEFAULT 0,
  "deadline" timestamptz(6),
  "enabled" bool NOT NULL DEFAULT true,
  "deleted" bool NOT NULL DEFAULT false,
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."ct_invite_code" OWNER TO "dev";
COMMENT ON COLUMN "public"."ct_invite_code"."code" IS '名称';
COMMENT ON COLUMN "public"."ct_invite_code"."brief" IS '描述';
COMMENT ON COLUMN "public"."ct_invite_code"."max_limit" IS '最大限制';
COMMENT ON COLUMN "public"."ct_invite_code"."register_num" IS '注册数量';
COMMENT ON COLUMN "public"."ct_invite_code"."deadline" IS '有效期';
COMMENT ON COLUMN "public"."ct_invite_code"."enabled" IS '是否启用';
COMMENT ON COLUMN "public"."ct_invite_code"."deleted" IS '是否删除';
COMMENT ON COLUMN "public"."ct_invite_code"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."ct_invite_code"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."ct_invite_code"."operator" IS '操作者';
COMMENT ON COLUMN "public"."ct_invite_code"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."ct_invite_code"."version" IS '版本号';
COMMENT ON COLUMN "public"."ct_invite_code"."desc" IS '描述';
COMMENT ON TABLE "public"."ct_invite_code" IS '邀请码表';

-- ----------------------------
-- Records of ct_invite_code
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for ct_menu
-- ----------------------------
DROP TABLE IF EXISTS "public"."ct_menu";
CREATE TABLE "public"."ct_menu" (
  "name" varchar(500) COLLATE "pg_catalog"."default" NOT NULL,
  "code" varchar(500) COLLATE "pg_catalog"."default" NOT NULL,
  "enabled" bool NOT NULL DEFAULT true,
  "parent_id" varchar(40) COLLATE "pg_catalog"."default",
  "url" varchar(500) COLLATE "pg_catalog"."default",
  "icon" varchar(500) COLLATE "pg_catalog"."default",
  "seq" int4 NOT NULL DEFAULT 0,
  "type" varchar(40) COLLATE "pg_catalog"."default" NOT NULL,
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."ct_menu" OWNER TO "dev";
COMMENT ON COLUMN "public"."ct_menu"."name" IS '菜单名称';
COMMENT ON COLUMN "public"."ct_menu"."code" IS '菜单编码';
COMMENT ON COLUMN "public"."ct_menu"."enabled" IS '是否启用';
COMMENT ON COLUMN "public"."ct_menu"."parent_id" IS '父级菜单ID';
COMMENT ON COLUMN "public"."ct_menu"."url" IS '菜单URL';
COMMENT ON COLUMN "public"."ct_menu"."icon" IS '菜单图标';
COMMENT ON COLUMN "public"."ct_menu"."seq" IS '排序';
COMMENT ON COLUMN "public"."ct_menu"."type" IS '菜单类型';
COMMENT ON COLUMN "public"."ct_menu"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."ct_menu"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."ct_menu"."operator" IS '操作者';
COMMENT ON COLUMN "public"."ct_menu"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."ct_menu"."version" IS '版本号';
COMMENT ON COLUMN "public"."ct_menu"."desc" IS '描述';
COMMENT ON TABLE "public"."ct_menu" IS '菜单表';

-- ----------------------------
-- Records of ct_menu
-- ----------------------------
BEGIN;
INSERT INTO "public"."ct_menu" ("name", "code", "enabled", "parent_id", "url", "icon", "seq", "type", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('系统管理', 'SYSTEM', 't', NULL, '/sys', 'fluent:settings-20-regular', 1, 'AGGREGATION', '5b37f17e-e31b-44fb-8b62-81c85dd0a67b', '2025-07-31 14:26:15.871574+08', '2026-04-10 21:24:09.161019+08', NULL, NULL, 8, NULL);
INSERT INTO "public"."ct_menu" ("name", "code", "enabled", "parent_id", "url", "icon", "seq", "type", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('角色管理', 'SYSTEM_ROLE', 't', '5b37f17e-e31b-44fb-8b62-81c85dd0a67b', '/sys/role', 'fluent:people-team-20-regular', 1, 'NORMAL', 'e9c890c3-cf30-41c2-9d40-f0cdc962d377', '2025-07-31 14:29:58.002233+08', '2026-04-10 21:24:09.302127+08', NULL, NULL, 8, NULL);
INSERT INTO "public"."ct_menu" ("name", "code", "enabled", "parent_id", "url", "icon", "seq", "type", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('菜单管理', 'SYSTEM_MENU', 't', '5b37f17e-e31b-44fb-8b62-81c85dd0a67b', '/sys/menu', 'fluent:list-20-regular', 2, 'NORMAL', '2dcac4bb-437d-4abf-933c-74c3ff471310', '2025-07-31 15:01:55.449406+08', '2026-04-10 21:24:09.440188+08', NULL, NULL, 8, NULL);
INSERT INTO "public"."ct_menu" ("name", "code", "enabled", "parent_id", "url", "icon", "seq", "type", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('功能权限', 'SYSTEM_PERMISSION', 't', '5b37f17e-e31b-44fb-8b62-81c85dd0a67b', '/sys/permission', 'fluent:shield-lock-20-regular', 3, 'NORMAL', 'f3327930-ccb8-4935-93b4-9259ee25dea3', '2025-07-31 15:09:00.586414+08', '2026-04-10 21:24:09.578557+08', NULL, NULL, 8, NULL);
INSERT INTO "public"."ct_menu" ("name", "code", "enabled", "parent_id", "url", "icon", "seq", "type", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('人员管理', 'SYSTEM_PEOPLE', 't', '5b37f17e-e31b-44fb-8b62-81c85dd0a67b', '/sys/people', 'fluent:person-20-regular', 4, 'NORMAL', 'ba72addc-1df1-4ec9-98a8-5da36247174c', '2025-07-31 15:10:00.408475+08', '2026-04-10 21:24:09.714464+08', NULL, NULL, 8, NULL);
INSERT INTO "public"."ct_menu" ("name", "code", "enabled", "parent_id", "url", "icon", "seq", "type", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('组织管理', 'SYSTEM_ORGANIZATION', 't', '5b37f17e-e31b-44fb-8b62-81c85dd0a67b', '/sys/organization', 'fluent:organization-20-regular', 5, 'NORMAL', '909beff8-b60f-4ff1-a7d2-7934a6189e46', '2025-07-31 15:11:15.816295+08', '2026-04-10 21:24:09.850526+08', NULL, NULL, 8, NULL);
INSERT INTO "public"."ct_menu" ("name", "code", "enabled", "parent_id", "url", "icon", "seq", "type", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('部门管理', 'SYSTEM_DEPT', 't', '5b37f17e-e31b-44fb-8b62-81c85dd0a67b', '/sys/dept', 'fluent:building-20-regular', 6, 'NORMAL', 'cfcb312e-ce60-4a93-87b1-4da44739a5bb', '2025-07-31 15:12:00.726679+08', '2026-04-10 21:24:09.993416+08', NULL, NULL, 8, NULL);
INSERT INTO "public"."ct_menu" ("name", "code", "enabled", "parent_id", "url", "icon", "seq", "type", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('邀请码管理', 'INVITE', 't', '5b37f17e-e31b-44fb-8b62-81c85dd0a67b', '/sys/invite', 'fluent:share-multiple-20-regular', 7, 'NORMAL', '0247782d-1229-48f6-95da-31089d6711b4', '2025-08-26 09:13:21.373205+08', '2026-04-10 21:24:10.140714+08', NULL, NULL, 6, NULL);
INSERT INTO "public"."ct_menu" ("name", "code", "enabled", "parent_id", "url", "icon", "seq", "type", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('测验', 'QUIZ', 't', NULL, '/quiz', 'fluent:quiz-new-20-filled', 2, 'AGGREGATION', '4a19a774-3f60-482c-9fba-ca5931dd91b9', '2026-04-10 21:20:00.098257+08', '2026-04-10 21:24:10.282052+08', NULL, NULL, 2, NULL);
INSERT INTO "public"."ct_menu" ("name", "code", "enabled", "parent_id", "url", "icon", "seq", "type", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('测验管理', 'QUIZ_LIST', 't', '4a19a774-3f60-482c-9fba-ca5931dd91b9', '/quiz/list', 'fluent:quiz-new-20-filled', 1, 'NORMAL', '423104ef-a8e3-4ac0-b6f7-2f915aa263a8', '2026-04-10 21:20:13.065979+08', '2026-04-10 21:24:10.421596+08', NULL, NULL, 2, NULL);
INSERT INTO "public"."ct_menu" ("name", "code", "enabled", "parent_id", "url", "icon", "seq", "type", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('Token管理', 'TOKEN_LIST', 't', '4a19a774-3f60-482c-9fba-ca5931dd91b9', '/quiz/tokens', 'fluent:key-20-filled', 3, 'NORMAL', '4518c7c1-8571-4582-a843-fc207862defe', '2026-04-10 21:22:05.180026+08', '2026-04-10 21:24:10.695687+08', NULL, NULL, 2, NULL);
COMMIT;

-- ----------------------------
-- Table structure for ct_organization
-- ----------------------------
DROP TABLE IF EXISTS "public"."ct_organization";
CREATE TABLE "public"."ct_organization" (
  "name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "code" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "category" varchar(255) COLLATE "pg_catalog"."default",
  "address" varchar(500) COLLATE "pg_catalog"."default",
  "parent_id" varchar(40) COLLATE "pg_catalog"."default",
  "seq" int4 NOT NULL,
  "enabled" bool NOT NULL,
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."ct_organization" OWNER TO "dev";
COMMENT ON COLUMN "public"."ct_organization"."name" IS '组织名称';
COMMENT ON COLUMN "public"."ct_organization"."code" IS '组织编码';
COMMENT ON COLUMN "public"."ct_organization"."category" IS '组织类型';
COMMENT ON COLUMN "public"."ct_organization"."address" IS '地址';
COMMENT ON COLUMN "public"."ct_organization"."parent_id" IS '父级组织ID';
COMMENT ON COLUMN "public"."ct_organization"."seq" IS '排序';
COMMENT ON COLUMN "public"."ct_organization"."enabled" IS '是否启用';
COMMENT ON COLUMN "public"."ct_organization"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."ct_organization"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."ct_organization"."operator" IS '操作者';
COMMENT ON COLUMN "public"."ct_organization"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."ct_organization"."version" IS '版本号';
COMMENT ON COLUMN "public"."ct_organization"."desc" IS '描述';
COMMENT ON TABLE "public"."ct_organization" IS '组织表';

-- ----------------------------
-- Records of ct_organization
-- ----------------------------
BEGIN;
INSERT INTO "public"."ct_organization" ("name", "code", "category", "address", "parent_id", "seq", "enabled", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('默认根组织', 'FUN_QUIZ', 'COMPANY', NULL, NULL, 1, 't', '421d02a8-a547-4568-8b04-2921d1a58b9a', '2026-01-15 15:53:24+08', '2026-04-22 15:58:38.144911+08', NULL, NULL, 4, NULL);
COMMIT;

-- ----------------------------
-- Table structure for ct_permission
-- ----------------------------
DROP TABLE IF EXISTS "public"."ct_permission";
CREATE TABLE "public"."ct_permission" (
  "name" varchar(500) COLLATE "pg_catalog"."default" NOT NULL,
  "code" varchar(500) COLLATE "pg_catalog"."default" NOT NULL,
  "resource_category" "public"."enumresourcepermissioncategory" NOT NULL,
  "resource_id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL,
  "enabled" bool NOT NULL DEFAULT true,
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."ct_permission" OWNER TO "dev";
COMMENT ON COLUMN "public"."ct_permission"."name" IS '权限名称';
COMMENT ON COLUMN "public"."ct_permission"."code" IS '权限编码';
COMMENT ON COLUMN "public"."ct_permission"."resource_category" IS '权限关联资源分类';
COMMENT ON COLUMN "public"."ct_permission"."resource_id" IS '权限关联资源ID';
COMMENT ON COLUMN "public"."ct_permission"."enabled" IS '是否启用';
COMMENT ON COLUMN "public"."ct_permission"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."ct_permission"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."ct_permission"."operator" IS '操作者';
COMMENT ON COLUMN "public"."ct_permission"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."ct_permission"."version" IS '版本号';
COMMENT ON COLUMN "public"."ct_permission"."desc" IS '描述';
COMMENT ON TABLE "public"."ct_permission" IS '权限表';

-- ----------------------------
-- Records of ct_permission
-- ----------------------------
BEGIN;
INSERT INTO "public"."ct_permission" ("name", "code", "resource_category", "resource_id", "enabled", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('角色管理', 'ROLE', 'MENU', 'e9c890c3-cf30-41c2-9d40-f0cdc962d377', 't', '9aa16be5-4271-4d6d-8d37-5ca9e0b7582a', '2025-08-26 08:58:20.938571+08', '2025-08-26 08:58:20.938571+08', NULL, NULL, 1, NULL);
INSERT INTO "public"."ct_permission" ("name", "code", "resource_category", "resource_id", "enabled", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('菜单管理', 'MENU', 'MENU', '2dcac4bb-437d-4abf-933c-74c3ff471310', 't', 'efe6af53-2c51-4d78-a4b3-94ccd544e0c5', '2025-08-26 08:59:59.302693+08', '2025-08-26 08:59:59.302693+08', NULL, NULL, 1, NULL);
INSERT INTO "public"."ct_permission" ("name", "code", "resource_category", "resource_id", "enabled", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('功能权限', 'PERMISSION', 'MENU', 'f3327930-ccb8-4935-93b4-9259ee25dea3', 't', '204978e6-99d5-41f2-b3bb-74a3921d6658', '2025-08-26 09:03:40.301824+08', '2025-08-26 09:03:40.301824+08', NULL, NULL, 1, NULL);
INSERT INTO "public"."ct_permission" ("name", "code", "resource_category", "resource_id", "enabled", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('组织管理', 'ORGANIZATION', 'MENU', '909beff8-b60f-4ff1-a7d2-7934a6189e46', 't', 'fdb2c2e6-e5ea-43df-8df0-320b69cd218c', '2025-08-26 09:07:26.524059+08', '2025-09-04 09:38:53.237215+08', NULL, NULL, 2, NULL);
INSERT INTO "public"."ct_permission" ("name", "code", "resource_category", "resource_id", "enabled", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('部门管理', 'DEPT', 'MENU', 'cfcb312e-ce60-4a93-87b1-4da44739a5bb', 't', 'aa973772-9471-4384-a891-b5484a921224', '2025-08-26 09:08:28.4167+08', '2025-09-04 09:39:30.536363+08', NULL, NULL, 2, NULL);
INSERT INTO "public"."ct_permission" ("name", "code", "resource_category", "resource_id", "enabled", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('邀请码管理', 'INVITE', 'MENU', '0247782d-1229-48f6-95da-31089d6711b4', 't', '2e0dc36e-3b63-4598-bd41-b8086fa2f845', '2025-08-26 09:14:19.187858+08', '2025-09-04 09:41:12.544646+08', NULL, NULL, 2, NULL);
INSERT INTO "public"."ct_permission" ("name", "code", "resource_category", "resource_id", "enabled", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('人员管理', 'PEOPLE', 'MENU', 'ba72addc-1df1-4ec9-98a8-5da36247174c', 't', '47ce7a9e-6c82-416a-8b03-155c40588c2e', '2025-08-26 09:06:02.757836+08', '2026-02-02 09:26:17.613068+08', NULL, NULL, 3, NULL);
INSERT INTO "public"."ct_permission" ("name", "code", "resource_category", "resource_id", "enabled", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('Token管理', 'TOKEN_LIST', 'MENU', '4518c7c1-8571-4582-a843-fc207862defe', 't', 'c1bd603e-4040-4ae6-85ab-4e3417b281b7', '2026-04-10 21:22:48.294686+08', '2026-04-10 23:03:14.982873+08', NULL, NULL, 2, NULL);
INSERT INTO "public"."ct_permission" ("name", "code", "resource_category", "resource_id", "enabled", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('测验管理', 'QUIZ_LIST', 'MENU', '423104ef-a8e3-4ac0-b6f7-2f915aa263a8', 't', '284a8055-ed05-4e7b-a46d-98a2c5cb3418', '2026-04-10 21:22:31.189339+08', '2026-04-10 23:03:24.53572+08', NULL, NULL, 2, NULL);
COMMIT;

-- ----------------------------
-- Table structure for ct_permission_assign
-- ----------------------------
DROP TABLE IF EXISTS "public"."ct_permission_assign";
CREATE TABLE "public"."ct_permission_assign" (
  "grant_type" "public"."enumpermissionassigngranttype" NOT NULL,
  "grant_object_id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL,
  "grantee_type" "public"."enumpermissionassigngranteetype" NOT NULL,
  "grantee_object_id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL,
  "permission_id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL,
  "start_time" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "policy" "public"."enumpermissionassignpolicy",
  "end_time" timestamptz(6),
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."ct_permission_assign" OWNER TO "dev";
COMMENT ON COLUMN "public"."ct_permission_assign"."grant_type" IS '授权类型';
COMMENT ON COLUMN "public"."ct_permission_assign"."grant_object_id" IS '授权对象ID';
COMMENT ON COLUMN "public"."ct_permission_assign"."grantee_type" IS '被授权类型';
COMMENT ON COLUMN "public"."ct_permission_assign"."grantee_object_id" IS '被授权对象ID';
COMMENT ON COLUMN "public"."ct_permission_assign"."permission_id" IS '权限ID';
COMMENT ON COLUMN "public"."ct_permission_assign"."start_time" IS '授权开始时间';
COMMENT ON COLUMN "public"."ct_permission_assign"."policy" IS '授权策略';
COMMENT ON COLUMN "public"."ct_permission_assign"."end_time" IS '授权结束时间';
COMMENT ON COLUMN "public"."ct_permission_assign"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."ct_permission_assign"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."ct_permission_assign"."operator" IS '操作者';
COMMENT ON COLUMN "public"."ct_permission_assign"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."ct_permission_assign"."version" IS '版本号';
COMMENT ON COLUMN "public"."ct_permission_assign"."desc" IS '描述';
COMMENT ON TABLE "public"."ct_permission_assign" IS '权限分配表';

-- ----------------------------
-- Records of ct_permission_assign
-- ----------------------------
BEGIN;
INSERT INTO "public"."ct_permission_assign" ("grant_type", "grant_object_id", "grantee_type", "grantee_object_id", "permission_id", "start_time", "policy", "end_time", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('MENU', 'e9c890c3-cf30-41c2-9d40-f0cdc962d377', 'ROLE', 'd9f67450-0fb9-4e2e-94cb-db89b69dcc07', '9aa16be5-4271-4d6d-8d37-5ca9e0b7582a', '2025-08-26 08:57:59.272+08', 'ALLOW', NULL, '06ddd1d1-4c0d-4706-b464-c1e098f55e04', '2025-08-26 08:58:20.938571+08', '2025-08-26 08:58:20.938571+08', NULL, NULL, 1, NULL);
INSERT INTO "public"."ct_permission_assign" ("grant_type", "grant_object_id", "grantee_type", "grantee_object_id", "permission_id", "start_time", "policy", "end_time", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('MENU', '2dcac4bb-437d-4abf-933c-74c3ff471310', 'ROLE', 'd9f67450-0fb9-4e2e-94cb-db89b69dcc07', 'efe6af53-2c51-4d78-a4b3-94ccd544e0c5', '2025-08-26 08:59:47.319+08', 'ALLOW', NULL, 'be376f9b-8f9b-40f3-b4a8-64ebb4b82b8c', '2025-08-26 08:59:59.302693+08', '2025-08-26 08:59:59.302693+08', NULL, NULL, 1, NULL);
INSERT INTO "public"."ct_permission_assign" ("grant_type", "grant_object_id", "grantee_type", "grantee_object_id", "permission_id", "start_time", "policy", "end_time", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('MENU', 'f3327930-ccb8-4935-93b4-9259ee25dea3', 'ROLE', 'd9f67450-0fb9-4e2e-94cb-db89b69dcc07', '204978e6-99d5-41f2-b3bb-74a3921d6658', '2025-08-26 09:03:33.337+08', 'ALLOW', NULL, 'b7534929-33e0-4582-870c-0c6c1b5b69e8', '2025-08-26 09:03:40.301824+08', '2025-08-26 09:03:40.301824+08', NULL, NULL, 1, NULL);
INSERT INTO "public"."ct_permission_assign" ("grant_type", "grant_object_id", "grantee_type", "grantee_object_id", "permission_id", "start_time", "policy", "end_time", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('MENU', '909beff8-b60f-4ff1-a7d2-7934a6189e46', 'ROLE', 'd9f67450-0fb9-4e2e-94cb-db89b69dcc07', 'fdb2c2e6-e5ea-43df-8df0-320b69cd218c', '2025-08-26 09:07:14.287+08', 'ALLOW', NULL, '816288ed-4964-4895-abe6-79dc74e54c95', '2025-08-26 09:07:26.524059+08', '2025-08-26 09:07:26.524059+08', NULL, NULL, 1, NULL);
INSERT INTO "public"."ct_permission_assign" ("grant_type", "grant_object_id", "grantee_type", "grantee_object_id", "permission_id", "start_time", "policy", "end_time", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('MENU', 'cfcb312e-ce60-4a93-87b1-4da44739a5bb', 'ROLE', 'd9f67450-0fb9-4e2e-94cb-db89b69dcc07', 'aa973772-9471-4384-a891-b5484a921224', '2025-08-26 09:08:08.04+08', 'ALLOW', NULL, '8a100c23-3a83-44a7-ba9d-1d5771e10c31', '2025-08-26 09:08:28.4167+08', '2025-08-26 09:08:28.4167+08', NULL, NULL, 1, NULL);
INSERT INTO "public"."ct_permission_assign" ("grant_type", "grant_object_id", "grantee_type", "grantee_object_id", "permission_id", "start_time", "policy", "end_time", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('MENU', 'cfcb312e-ce60-4a93-87b1-4da44739a5bb', 'ROLE', 'a16ad367-c8ae-48be-a545-d59492a960e5', 'aa973772-9471-4384-a891-b5484a921224', '2025-08-26 09:08:17.487+08', 'ALLOW', NULL, '9ab961da-79a9-436f-bfbe-30d0ba468b30', '2025-08-26 09:08:28.4167+08', '2025-08-26 09:08:28.4167+08', NULL, NULL, 1, NULL);
INSERT INTO "public"."ct_permission_assign" ("grant_type", "grant_object_id", "grantee_type", "grantee_object_id", "permission_id", "start_time", "policy", "end_time", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('MENU', 'cfcb312e-ce60-4a93-87b1-4da44739a5bb', 'ROLE', 'c98ab1bc-5c6a-408b-adc6-806103c0a565', 'aa973772-9471-4384-a891-b5484a921224', '2025-09-04 09:39:21.112+08', 'ALLOW', NULL, 'fc7bfd7d-2b0a-4c37-87fa-f8031e52a73f', '2025-09-04 09:39:31.960586+08', '2025-09-04 09:39:31.960586+08', NULL, NULL, 1, NULL);
INSERT INTO "public"."ct_permission_assign" ("grant_type", "grant_object_id", "grantee_type", "grantee_object_id", "permission_id", "start_time", "policy", "end_time", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('MENU', '0247782d-1229-48f6-95da-31089d6711b4', 'ROLE', 'd9f67450-0fb9-4e2e-94cb-db89b69dcc07', '2e0dc36e-3b63-4598-bd41-b8086fa2f845', '2025-08-26 09:14:06.896+08', 'ALLOW', NULL, '11faeea5-dd38-4b6d-b9ba-848551984814', '2025-08-26 09:14:19.187858+08', '2025-08-26 09:14:19.187858+08', NULL, NULL, 1, NULL);
INSERT INTO "public"."ct_permission_assign" ("grant_type", "grant_object_id", "grantee_type", "grantee_object_id", "permission_id", "start_time", "policy", "end_time", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('MENU', '0247782d-1229-48f6-95da-31089d6711b4', 'ROLE', 'a16ad367-c8ae-48be-a545-d59492a960e5', '2e0dc36e-3b63-4598-bd41-b8086fa2f845', '2025-08-26 09:14:11.127+08', 'ALLOW', NULL, '15aa585d-82ab-437e-b5d5-568747c142d1', '2025-08-26 09:14:19.187858+08', '2025-08-26 09:14:19.187858+08', NULL, NULL, 1, NULL);
INSERT INTO "public"."ct_permission_assign" ("grant_type", "grant_object_id", "grantee_type", "grantee_object_id", "permission_id", "start_time", "policy", "end_time", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('MENU', '0247782d-1229-48f6-95da-31089d6711b4', 'ROLE', 'c98ab1bc-5c6a-408b-adc6-806103c0a565', '2e0dc36e-3b63-4598-bd41-b8086fa2f845', '2025-09-04 09:41:06.784+08', 'ALLOW', NULL, '3eab0b57-3af9-40e2-a63a-9bf75666bca6', '2025-09-04 09:41:13.989119+08', '2025-09-04 09:41:13.989119+08', NULL, NULL, 1, NULL);
INSERT INTO "public"."ct_permission_assign" ("grant_type", "grant_object_id", "grantee_type", "grantee_object_id", "permission_id", "start_time", "policy", "end_time", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('MENU', 'ba72addc-1df1-4ec9-98a8-5da36247174c', 'ROLE', 'd9f67450-0fb9-4e2e-94cb-db89b69dcc07', '47ce7a9e-6c82-416a-8b03-155c40588c2e', '2025-08-26 09:05:38.639+08', 'ALLOW', NULL, 'a4c7ce60-df76-4258-811f-79742344b9ad', '2025-08-26 09:06:02.757836+08', '2025-08-26 09:06:02.757836+08', NULL, NULL, 1, NULL);
INSERT INTO "public"."ct_permission_assign" ("grant_type", "grant_object_id", "grantee_type", "grantee_object_id", "permission_id", "start_time", "policy", "end_time", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('MENU', 'ba72addc-1df1-4ec9-98a8-5da36247174c', 'ROLE', 'a16ad367-c8ae-48be-a545-d59492a960e5', '47ce7a9e-6c82-416a-8b03-155c40588c2e', '2025-08-26 09:05:47.631+08', 'ALLOW', NULL, 'f79221a4-4ebb-4a2e-9185-eefc3fba7414', '2025-08-26 09:06:02.757836+08', '2025-08-26 09:06:02.757836+08', NULL, NULL, 1, NULL);
INSERT INTO "public"."ct_permission_assign" ("grant_type", "grant_object_id", "grantee_type", "grantee_object_id", "permission_id", "start_time", "policy", "end_time", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('MENU', 'ba72addc-1df1-4ec9-98a8-5da36247174c', 'ROLE', 'c98ab1bc-5c6a-408b-adc6-806103c0a565', '47ce7a9e-6c82-416a-8b03-155c40588c2e', '2025-09-04 09:37:43.872+08', 'ALLOW', NULL, 'e7420df4-b33f-4731-a7f6-ae092a7d2670', '2025-09-04 09:37:50.586554+08', '2025-09-04 09:37:50.586554+08', NULL, NULL, 1, NULL);
INSERT INTO "public"."ct_permission_assign" ("grant_type", "grant_object_id", "grantee_type", "grantee_object_id", "permission_id", "start_time", "policy", "end_time", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('MENU', 'ba72addc-1df1-4ec9-98a8-5da36247174c', 'ROLE', 'b3b5fe0c-1b84-488e-a3bf-19b2582c4af7', '47ce7a9e-6c82-416a-8b03-155c40588c2e', '2026-02-02 09:25:50.99+08', 'ALLOW', NULL, '3908eaaf-65f1-4474-9202-fa8301e03d23', '2026-02-02 09:26:26.774022+08', '2026-02-02 09:26:26.774022+08', NULL, NULL, 1, NULL);
INSERT INTO "public"."ct_permission_assign" ("grant_type", "grant_object_id", "grantee_type", "grantee_object_id", "permission_id", "start_time", "policy", "end_time", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('MENU', 'ba72addc-1df1-4ec9-98a8-5da36247174c', 'ROLE', '702df378-717c-44bc-a0e1-ceeacf5b960c', '47ce7a9e-6c82-416a-8b03-155c40588c2e', '2026-02-02 09:26:01.75+08', 'ALLOW', NULL, 'ddae6130-b39f-4828-84e4-5c99f4f110bd', '2026-02-02 09:26:26.774022+08', '2026-02-02 09:26:26.774022+08', NULL, NULL, 1, NULL);
INSERT INTO "public"."ct_permission_assign" ("grant_type", "grant_object_id", "grantee_type", "grantee_object_id", "permission_id", "start_time", "policy", "end_time", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('MENU', 'ba72addc-1df1-4ec9-98a8-5da36247174c', 'ROLE', '9b5a9117-76bd-4873-82c9-e16b60717337', '47ce7a9e-6c82-416a-8b03-155c40588c2e', '2026-02-02 09:26:10.583+08', 'ALLOW', NULL, 'fbfa0ae1-0cee-4fee-a67b-d4230eaa5d66', '2026-02-02 09:26:26.774022+08', '2026-02-02 09:26:26.774022+08', NULL, NULL, 1, NULL);
INSERT INTO "public"."ct_permission_assign" ("grant_type", "grant_object_id", "grantee_type", "grantee_object_id", "permission_id", "start_time", "policy", "end_time", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('MENU', '4518c7c1-8571-4582-a843-fc207862defe', 'ROLE', 'd9f67450-0fb9-4e2e-94cb-db89b69dcc07', 'c1bd603e-4040-4ae6-85ab-4e3417b281b7', '2026-04-10 21:22:43.602+08', 'ALLOW', NULL, '1db43480-dae4-47f4-b53e-0bca359b87cc', '2026-04-10 21:22:48.294686+08', '2026-04-10 21:22:48.294686+08', NULL, NULL, 1, NULL);
INSERT INTO "public"."ct_permission_assign" ("grant_type", "grant_object_id", "grantee_type", "grantee_object_id", "permission_id", "start_time", "policy", "end_time", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('MENU', '4518c7c1-8571-4582-a843-fc207862defe', 'ROLE', 'c39d5ccf-75e9-49ac-adbd-18b52c016c02', 'c1bd603e-4040-4ae6-85ab-4e3417b281b7', '2026-04-10 23:03:09.55+08', 'ALLOW', NULL, '03bda5a4-02b8-4a69-8733-50fda9c2f79f', '2026-04-10 23:03:15.194907+08', '2026-04-10 23:03:15.194907+08', NULL, NULL, 1, NULL);
INSERT INTO "public"."ct_permission_assign" ("grant_type", "grant_object_id", "grantee_type", "grantee_object_id", "permission_id", "start_time", "policy", "end_time", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('MENU', '423104ef-a8e3-4ac0-b6f7-2f915aa263a8', 'ROLE', 'd9f67450-0fb9-4e2e-94cb-db89b69dcc07', '284a8055-ed05-4e7b-a46d-98a2c5cb3418', '2026-04-10 21:22:25.649+08', 'ALLOW', NULL, '439e285c-c2ad-4df8-a3cc-896f8b5e5f04', '2026-04-10 21:22:31.189339+08', '2026-04-10 21:22:31.189339+08', NULL, NULL, 1, NULL);
INSERT INTO "public"."ct_permission_assign" ("grant_type", "grant_object_id", "grantee_type", "grantee_object_id", "permission_id", "start_time", "policy", "end_time", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('MENU', '423104ef-a8e3-4ac0-b6f7-2f915aa263a8', 'ROLE', 'c39d5ccf-75e9-49ac-adbd-18b52c016c02', '284a8055-ed05-4e7b-a46d-98a2c5cb3418', '2026-04-10 23:03:19.41+08', 'ALLOW', NULL, 'b040d121-a94f-49c7-adbf-dbc5b8545fa9', '2026-04-10 23:03:24.741762+08', '2026-04-10 23:03:24.741762+08', NULL, NULL, 1, NULL);
COMMIT;

-- ----------------------------
-- Table structure for ct_robot
-- ----------------------------
DROP TABLE IF EXISTS "public"."ct_robot";
CREATE TABLE "public"."ct_robot" (
  "name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "category" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "enabled" bool NOT NULL,
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."ct_robot" OWNER TO "dev";
COMMENT ON COLUMN "public"."ct_robot"."name" IS '机器人名称';
COMMENT ON COLUMN "public"."ct_robot"."category" IS '机器人类型';
COMMENT ON COLUMN "public"."ct_robot"."enabled" IS '是否启用';
COMMENT ON COLUMN "public"."ct_robot"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."ct_robot"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."ct_robot"."operator" IS '操作者';
COMMENT ON COLUMN "public"."ct_robot"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."ct_robot"."version" IS '版本号';
COMMENT ON COLUMN "public"."ct_robot"."desc" IS '描述';
COMMENT ON TABLE "public"."ct_robot" IS '同步日志表';

-- ----------------------------
-- Records of ct_robot
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for ct_role
-- ----------------------------
DROP TABLE IF EXISTS "public"."ct_role";
CREATE TABLE "public"."ct_role" (
  "name" varchar(500) COLLATE "pg_catalog"."default" NOT NULL,
  "brief" text COLLATE "pg_catalog"."default",
  "code" varchar(500) COLLATE "pg_catalog"."default" NOT NULL,
  "enabled" bool NOT NULL DEFAULT true,
  "seq" int4 NOT NULL,
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."ct_role" OWNER TO "dev";
COMMENT ON COLUMN "public"."ct_role"."name" IS '角色名称';
COMMENT ON COLUMN "public"."ct_role"."brief" IS '描述';
COMMENT ON COLUMN "public"."ct_role"."code" IS '角色编码';
COMMENT ON COLUMN "public"."ct_role"."enabled" IS '是否启用';
COMMENT ON COLUMN "public"."ct_role"."seq" IS '排序';
COMMENT ON COLUMN "public"."ct_role"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."ct_role"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."ct_role"."operator" IS '操作者';
COMMENT ON COLUMN "public"."ct_role"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."ct_role"."version" IS '版本号';
COMMENT ON COLUMN "public"."ct_role"."desc" IS '描述';
COMMENT ON TABLE "public"."ct_role" IS '角色表';

-- ----------------------------
-- Records of ct_role
-- ----------------------------
BEGIN;
INSERT INTO "public"."ct_role" ("name", "brief", "code", "enabled", "seq", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('超级管理员', '系统最高权限管理员，拥有所有功能权限。', 'SUPER_ADMIN', 't', 1, 'd9f67450-0fb9-4e2e-94cb-db89b69dcc07', '2025-07-28 10:23:07.660982+08', '2025-07-28 10:23:07.660982+08', NULL, NULL, 1, NULL);
INSERT INTO "public"."ct_role" ("name", "brief", "code", "enabled", "seq", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('管理员', NULL, 'ADMIN', 't', 5, 'c39d5ccf-75e9-49ac-adbd-18b52c016c02', '2026-04-10 23:01:56.416912+08', '2026-04-10 23:01:56.416912+08', NULL, NULL, 1, NULL);
INSERT INTO "public"."ct_role" ("name", "brief", "code", "enabled", "seq", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('普通用户', '普通web端用户角色，拥有基础功能权限。', 'WEB_USER', 't', 4, '9b5a9117-76bd-4873-82c9-e16b60717337', '2025-07-28 10:23:30.927653+08', '2026-04-22 15:57:25.989283+08', NULL, NULL, 6, NULL);
COMMIT;

-- ----------------------------
-- Table structure for ct_transaction
-- ----------------------------
DROP TABLE IF EXISTS "public"."ct_transaction";
CREATE TABLE "public"."ct_transaction" (
  "current_user_info" jsonb,
  "start_time" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "end_time" timestamptz(6),
  "status" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "request_info" jsonb,
  "request_params" jsonb,
  "params" jsonb,
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."ct_transaction" OWNER TO "dev";
COMMENT ON COLUMN "public"."ct_transaction"."current_user_info" IS '当前用户信息';
COMMENT ON COLUMN "public"."ct_transaction"."start_time" IS '开始时间';
COMMENT ON COLUMN "public"."ct_transaction"."end_time" IS '结束时间';
COMMENT ON COLUMN "public"."ct_transaction"."status" IS '状态';
COMMENT ON COLUMN "public"."ct_transaction"."request_info" IS '请求信息';
COMMENT ON COLUMN "public"."ct_transaction"."request_params" IS '参数';
COMMENT ON COLUMN "public"."ct_transaction"."params" IS '其他参数';
COMMENT ON COLUMN "public"."ct_transaction"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."ct_transaction"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."ct_transaction"."operator" IS '操作者';
COMMENT ON COLUMN "public"."ct_transaction"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."ct_transaction"."version" IS '版本号';
COMMENT ON COLUMN "public"."ct_transaction"."desc" IS '描述';
COMMENT ON TABLE "public"."ct_transaction" IS '事务表';

-- ----------------------------
-- Records of ct_transaction
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for ct_transaction_log
-- ----------------------------
DROP TABLE IF EXISTS "public"."ct_transaction_log";
CREATE TABLE "public"."ct_transaction_log" (
  "transaction_id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL,
  "action" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "params" jsonb,
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."ct_transaction_log" OWNER TO "dev";
COMMENT ON COLUMN "public"."ct_transaction_log"."transaction_id" IS '事务ID';
COMMENT ON COLUMN "public"."ct_transaction_log"."action" IS '操作';
COMMENT ON COLUMN "public"."ct_transaction_log"."params" IS '参数';
COMMENT ON COLUMN "public"."ct_transaction_log"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."ct_transaction_log"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."ct_transaction_log"."operator" IS '操作者';
COMMENT ON COLUMN "public"."ct_transaction_log"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."ct_transaction_log"."version" IS '版本号';
COMMENT ON COLUMN "public"."ct_transaction_log"."desc" IS '描述';
COMMENT ON TABLE "public"."ct_transaction_log" IS '事务日志表';

-- ----------------------------
-- Records of ct_transaction_log
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for ct_union_user
-- ----------------------------
DROP TABLE IF EXISTS "public"."ct_union_user";
CREATE TABLE "public"."ct_union_user" (
  "name" varchar(255) COLLATE "pg_catalog"."default",
  "enabled" bool NOT NULL DEFAULT true,
  "is_deleted" bool NOT NULL DEFAULT false,
  "info" jsonb,
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."ct_union_user" OWNER TO "dev";
COMMENT ON COLUMN "public"."ct_union_user"."name" IS '名称';
COMMENT ON COLUMN "public"."ct_union_user"."enabled" IS '是否启用';
COMMENT ON COLUMN "public"."ct_union_user"."is_deleted" IS '是否删除';
COMMENT ON COLUMN "public"."ct_union_user"."info" IS '其它信息';
COMMENT ON COLUMN "public"."ct_union_user"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."ct_union_user"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."ct_union_user"."operator" IS '操作者';
COMMENT ON COLUMN "public"."ct_union_user"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."ct_union_user"."version" IS '版本号';
COMMENT ON COLUMN "public"."ct_union_user"."desc" IS '描述';
COMMENT ON TABLE "public"."ct_union_user" IS '联合用户表';

-- ----------------------------
-- Records of ct_union_user
-- ----------------------------
BEGIN;
INSERT INTO "public"."ct_union_user" ("name", "enabled", "is_deleted", "info", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('SuperAdmin', 't', 'f', NULL, 'c41d4cee-f239-4e59-83d5-40b05baf6926', '2026-01-15 16:34:23.40319+08', '2026-04-10 23:01:24.650384+08', NULL, NULL, 2, NULL);
COMMIT;

-- ----------------------------
-- Table structure for ct_union_user_user
-- ----------------------------
DROP TABLE IF EXISTS "public"."ct_union_user_user";
CREATE TABLE "public"."ct_union_user_user" (
  "union_user_id" varchar(40) COLLATE "pg_catalog"."default",
  "union_user_user_category" varchar(255) COLLATE "pg_catalog"."default",
  "union_user_user_id" varchar(40) COLLATE "pg_catalog"."default",
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."ct_union_user_user" OWNER TO "dev";
COMMENT ON COLUMN "public"."ct_union_user_user"."union_user_id" IS '联合用户id';
COMMENT ON COLUMN "public"."ct_union_user_user"."union_user_user_category" IS '用户类别, 企微用户、微信小程序用户、web用户等';
COMMENT ON COLUMN "public"."ct_union_user_user"."union_user_user_id" IS '用户id';
COMMENT ON COLUMN "public"."ct_union_user_user"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."ct_union_user_user"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."ct_union_user_user"."operator" IS '操作者';
COMMENT ON COLUMN "public"."ct_union_user_user"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."ct_union_user_user"."version" IS '版本号';
COMMENT ON COLUMN "public"."ct_union_user_user"."desc" IS '描述';
COMMENT ON TABLE "public"."ct_union_user_user" IS '联合用户用户表';

-- ----------------------------
-- Records of ct_union_user_user
-- ----------------------------
BEGIN;
INSERT INTO "public"."ct_union_user_user" ("union_user_id", "union_user_user_category", "union_user_user_id", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('c41d4cee-f239-4e59-83d5-40b05baf6926', 'WEB_USER', '9f91bf33-44c9-46de-affa-b499b5e5d8af', '57911f79-7972-4681-9759-ceabbd84679a', '2026-01-15 16:36:51.170138+08', '2026-04-10 23:01:24.796727+08', NULL, NULL, 2, NULL);
COMMIT;

-- ----------------------------
-- Table structure for ct_user_role
-- ----------------------------
DROP TABLE IF EXISTS "public"."ct_user_role";
CREATE TABLE "public"."ct_user_role" (
  "user_id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL,
  "user_category" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "role_id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL,
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."ct_user_role" OWNER TO "dev";
COMMENT ON COLUMN "public"."ct_user_role"."user_id" IS '用户id';
COMMENT ON COLUMN "public"."ct_user_role"."user_category" IS '用户类型，企微用户、web用户';
COMMENT ON COLUMN "public"."ct_user_role"."role_id" IS '角色id';
COMMENT ON COLUMN "public"."ct_user_role"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."ct_user_role"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."ct_user_role"."operator" IS '操作者';
COMMENT ON COLUMN "public"."ct_user_role"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."ct_user_role"."version" IS '版本号';
COMMENT ON COLUMN "public"."ct_user_role"."desc" IS '描述';
COMMENT ON TABLE "public"."ct_user_role" IS '用户角色表';

-- ----------------------------
-- Records of ct_user_role
-- ----------------------------
BEGIN;
INSERT INTO "public"."ct_user_role" ("user_id", "user_category", "role_id", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('9f91bf33-44c9-46de-affa-b499b5e5d8af', 'WEB_USER', '9b5a9117-76bd-4873-82c9-e16b60717337', '48ad7e8d-5e83-4323-9730-6646503e4d07', '2026-01-15 16:15:38.01322+08', '2026-01-15 16:15:38.01322+08', NULL, NULL, 1, NULL);
INSERT INTO "public"."ct_user_role" ("user_id", "user_category", "role_id", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('9f91bf33-44c9-46de-affa-b499b5e5d8af', 'WEB_USER', 'd9f67450-0fb9-4e2e-94cb-db89b69dcc07', '1a6670cd-52c7-4ef6-8262-e11d582f9328', '2026-01-15 16:19:45.140836+08', '2026-01-15 16:19:45.140836+08', NULL, NULL, 1, NULL);
INSERT INTO "public"."ct_user_role" ("user_id", "user_category", "role_id", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('9f91bf33-44c9-46de-affa-b499b5e5d8af', 'WEB_USER', 'c39d5ccf-75e9-49ac-adbd-18b52c016c02', '6755a7e0-5e4f-42f5-8d91-cd8ff785bc26', '2026-04-10 23:04:09.730217+08', '2026-04-10 23:04:09.730217+08', NULL, NULL, 1, NULL);
COMMIT;

-- ----------------------------
-- Table structure for ct_web_user
-- ----------------------------
DROP TABLE IF EXISTS "public"."ct_web_user";
CREATE TABLE "public"."ct_web_user" (
  "name" varchar(500) COLLATE "pg_catalog"."default" NOT NULL,
  "mobile" varchar(255) COLLATE "pg_catalog"."default",
  "email" varchar(255) COLLATE "pg_catalog"."default",
  "enabled" bool NOT NULL DEFAULT true,
  "avatar_file_info" jsonb,
  "password_salt" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "password_hash" varchar(500) COLLATE "pg_catalog"."default" NOT NULL,
  "try_count" int4 NOT NULL DEFAULT 0,
  "reset_password" bool NOT NULL DEFAULT false,
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."ct_web_user" OWNER TO "dev";
COMMENT ON COLUMN "public"."ct_web_user"."name" IS '用户名称';
COMMENT ON COLUMN "public"."ct_web_user"."mobile" IS '手机号';
COMMENT ON COLUMN "public"."ct_web_user"."email" IS '邮箱';
COMMENT ON COLUMN "public"."ct_web_user"."enabled" IS '是否启用';
COMMENT ON COLUMN "public"."ct_web_user"."avatar_file_info" IS '头像文件信息';
COMMENT ON COLUMN "public"."ct_web_user"."password_salt" IS '密码盐';
COMMENT ON COLUMN "public"."ct_web_user"."password_hash" IS '密码';
COMMENT ON COLUMN "public"."ct_web_user"."try_count" IS '登录失败次数';
COMMENT ON COLUMN "public"."ct_web_user"."reset_password" IS '是否重置密码';
COMMENT ON COLUMN "public"."ct_web_user"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."ct_web_user"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."ct_web_user"."operator" IS '操作者';
COMMENT ON COLUMN "public"."ct_web_user"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."ct_web_user"."version" IS '版本号';
COMMENT ON COLUMN "public"."ct_web_user"."desc" IS '描述';
COMMENT ON TABLE "public"."ct_web_user" IS '用户表';

-- ----------------------------
-- Records of ct_web_user
-- ----------------------------
BEGIN;
INSERT INTO "public"."ct_web_user" ("name", "mobile", "email", "enabled", "avatar_file_info", "password_salt", "password_hash", "try_count", "reset_password", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('SuperAdmin', NULL, NULL, 't', '{"url": null, "file_hash": null, "file_name": null, "file_size": null, "file_type": null, "bucket_name": null, "object_name": null, "file_info_id": null, "file_object_name": null}', '18f18246298be9f25aaf580c840d9f6a', '7acb7474cb4671568a23bad26366900ae6f1b6f2423def0d0fd3c41013bbe8e6', 0, 'f', '9f91bf33-44c9-46de-affa-b499b5e5d8af', '2026-01-15 16:15:38.01322+08', '2026-04-22 16:22:57.069283+08', NULL, NULL, 36, NULL);
COMMIT;

-- ----------------------------
-- Table structure for ct_web_user_dept
-- ----------------------------
DROP TABLE IF EXISTS "public"."ct_web_user_dept";
CREATE TABLE "public"."ct_web_user_dept" (
  "web_user_id" varchar(40) COLLATE "pg_catalog"."default",
  "dept_id" varchar(40) COLLATE "pg_catalog"."default",
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."ct_web_user_dept" OWNER TO "dev";
COMMENT ON COLUMN "public"."ct_web_user_dept"."web_user_id" IS 'web用户ID';
COMMENT ON COLUMN "public"."ct_web_user_dept"."dept_id" IS '部门ID';
COMMENT ON COLUMN "public"."ct_web_user_dept"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."ct_web_user_dept"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."ct_web_user_dept"."operator" IS '操作者';
COMMENT ON COLUMN "public"."ct_web_user_dept"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."ct_web_user_dept"."version" IS '版本号';
COMMENT ON COLUMN "public"."ct_web_user_dept"."desc" IS '描述';
COMMENT ON TABLE "public"."ct_web_user_dept" IS 'web用户所属部门表';

-- ----------------------------
-- Records of ct_web_user_dept
-- ----------------------------
BEGIN;
INSERT INTO "public"."ct_web_user_dept" ("web_user_id", "dept_id", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('9f91bf33-44c9-46de-affa-b499b5e5d8af', '75f02c0d-f1ff-48c6-9c5a-d8bbcfc18141', '733e8a54-5fef-4065-83c7-767968358dfa', '2026-01-15 16:15:38.01322+08', '2026-01-15 16:15:38.01322+08', NULL, NULL, 1, NULL);
COMMIT;

-- ----------------------------
-- Table structure for ct_web_user_organization
-- ----------------------------
DROP TABLE IF EXISTS "public"."ct_web_user_organization";
CREATE TABLE "public"."ct_web_user_organization" (
  "web_user_id" varchar(40) COLLATE "pg_catalog"."default",
  "organization_id" varchar(40) COLLATE "pg_catalog"."default",
  "id" varchar(40) COLLATE "pg_catalog"."default" NOT NULL DEFAULT uuid_generate_v4(),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "operator" varchar(255) COLLATE "pg_catalog"."default",
  "operator_category" varchar(255) COLLATE "pg_catalog"."default",
  "version" int4 NOT NULL DEFAULT 1,
  "desc" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."ct_web_user_organization" OWNER TO "dev";
COMMENT ON COLUMN "public"."ct_web_user_organization"."web_user_id" IS 'web用户ID';
COMMENT ON COLUMN "public"."ct_web_user_organization"."organization_id" IS '组织ID';
COMMENT ON COLUMN "public"."ct_web_user_organization"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."ct_web_user_organization"."updated_at" IS '更新时间';
COMMENT ON COLUMN "public"."ct_web_user_organization"."operator" IS '操作者';
COMMENT ON COLUMN "public"."ct_web_user_organization"."operator_category" IS '操作者类别';
COMMENT ON COLUMN "public"."ct_web_user_organization"."version" IS '版本号';
COMMENT ON COLUMN "public"."ct_web_user_organization"."desc" IS '描述';
COMMENT ON TABLE "public"."ct_web_user_organization" IS 'web用户所属组织表';

-- ----------------------------
-- Records of ct_web_user_organization
-- ----------------------------
BEGIN;
INSERT INTO "public"."ct_web_user_organization" ("web_user_id", "organization_id", "id", "created_at", "updated_at", "operator", "operator_category", "version", "desc") VALUES ('9f91bf33-44c9-46de-affa-b499b5e5d8af', '421d02a8-a547-4568-8b04-2921d1a58b9a', '52f5003d-2c8a-4662-8f7e-ea81b1d8468e', '2026-01-15 16:15:38.01322+08', '2026-01-15 16:15:38.01322+08', NULL, NULL, 1, NULL);
COMMIT;

-- ----------------------------
-- Function structure for uuid_generate_v1
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."uuid_generate_v1"();
CREATE FUNCTION "public"."uuid_generate_v1"()
  RETURNS "pg_catalog"."uuid" AS '$libdir/uuid-ossp', 'uuid_generate_v1'
  LANGUAGE c VOLATILE STRICT
  COST 1;
ALTER FUNCTION "public"."uuid_generate_v1"() OWNER TO "postgres";

-- ----------------------------
-- Function structure for uuid_generate_v1mc
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."uuid_generate_v1mc"();
CREATE FUNCTION "public"."uuid_generate_v1mc"()
  RETURNS "pg_catalog"."uuid" AS '$libdir/uuid-ossp', 'uuid_generate_v1mc'
  LANGUAGE c VOLATILE STRICT
  COST 1;
ALTER FUNCTION "public"."uuid_generate_v1mc"() OWNER TO "postgres";

-- ----------------------------
-- Function structure for uuid_generate_v3
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."uuid_generate_v3"("namespace" uuid, "name" text);
CREATE FUNCTION "public"."uuid_generate_v3"("namespace" uuid, "name" text)
  RETURNS "pg_catalog"."uuid" AS '$libdir/uuid-ossp', 'uuid_generate_v3'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION "public"."uuid_generate_v3"("namespace" uuid, "name" text) OWNER TO "postgres";

-- ----------------------------
-- Function structure for uuid_generate_v4
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."uuid_generate_v4"();
CREATE FUNCTION "public"."uuid_generate_v4"()
  RETURNS "pg_catalog"."uuid" AS '$libdir/uuid-ossp', 'uuid_generate_v4'
  LANGUAGE c VOLATILE STRICT
  COST 1;
ALTER FUNCTION "public"."uuid_generate_v4"() OWNER TO "postgres";

-- ----------------------------
-- Function structure for uuid_generate_v5
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."uuid_generate_v5"("namespace" uuid, "name" text);
CREATE FUNCTION "public"."uuid_generate_v5"("namespace" uuid, "name" text)
  RETURNS "pg_catalog"."uuid" AS '$libdir/uuid-ossp', 'uuid_generate_v5'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION "public"."uuid_generate_v5"("namespace" uuid, "name" text) OWNER TO "postgres";

-- ----------------------------
-- Function structure for uuid_nil
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."uuid_nil"();
CREATE FUNCTION "public"."uuid_nil"()
  RETURNS "pg_catalog"."uuid" AS '$libdir/uuid-ossp', 'uuid_nil'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION "public"."uuid_nil"() OWNER TO "postgres";

-- ----------------------------
-- Function structure for uuid_ns_dns
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."uuid_ns_dns"();
CREATE FUNCTION "public"."uuid_ns_dns"()
  RETURNS "pg_catalog"."uuid" AS '$libdir/uuid-ossp', 'uuid_ns_dns'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION "public"."uuid_ns_dns"() OWNER TO "postgres";

-- ----------------------------
-- Function structure for uuid_ns_oid
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."uuid_ns_oid"();
CREATE FUNCTION "public"."uuid_ns_oid"()
  RETURNS "pg_catalog"."uuid" AS '$libdir/uuid-ossp', 'uuid_ns_oid'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION "public"."uuid_ns_oid"() OWNER TO "postgres";

-- ----------------------------
-- Function structure for uuid_ns_url
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."uuid_ns_url"();
CREATE FUNCTION "public"."uuid_ns_url"()
  RETURNS "pg_catalog"."uuid" AS '$libdir/uuid-ossp', 'uuid_ns_url'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION "public"."uuid_ns_url"() OWNER TO "postgres";

-- ----------------------------
-- Function structure for uuid_ns_x500
-- ----------------------------
DROP FUNCTION IF EXISTS "public"."uuid_ns_x500"();
CREATE FUNCTION "public"."uuid_ns_x500"()
  RETURNS "pg_catalog"."uuid" AS '$libdir/uuid-ossp', 'uuid_ns_x500'
  LANGUAGE c IMMUTABLE STRICT
  COST 1;
ALTER FUNCTION "public"."uuid_ns_x500"() OWNER TO "postgres";

-- ----------------------------
-- View structure for view_backend_api
-- ----------------------------
DROP VIEW IF EXISTS "public"."view_backend_api";
CREATE VIEW "public"."view_backend_api" AS  SELECT name,
    code,
    enabled,
    url,
    ignore_auth,
    id,
    created_at,
    updated_at,
    operator,
    operator_category,
    version,
    "desc",
    regexp_replace(regexp_replace(url::text, '\{[^/]+\}'::text, ''::text, 'g'::text), '/+$'::text, ''::text, 'g'::text) AS cleaned_url
   FROM ct_backend_api cba;
ALTER TABLE "public"."view_backend_api" OWNER TO "dev";

-- ----------------------------
-- View structure for view_dept_tree
-- ----------------------------
DROP VIEW IF EXISTS "public"."view_dept_tree";
CREATE VIEW "public"."view_dept_tree" AS  WITH RECURSIVE dept_hierarchy AS (
         SELECT cd.organization_id,
            cd.id,
            cd.name,
            cd.code,
            cd.enabled,
            cd.category,
            cd.parent_id,
            cd.brief,
            cd.source_category,
            cd.source_id,
            cd.seq,
            1 AS level,
            ARRAY[cd.seq] AS seq_list,
            ARRAY[cd.name::text] AS name_list,
            ARRAY[cd.id::text] AS dept_id_list
           FROM ct_dept cd
          WHERE cd.parent_id IS NULL
        UNION ALL
         SELECT c.organization_id,
            c.id,
            c.name,
            c.code,
            c.enabled,
            c.category,
            c.parent_id,
            c.brief,
            c.source_category,
            c.source_id,
            c.seq,
            oh_1.level + 1 AS level,
            oh_1.seq_list || c.seq,
            oh_1.name_list || c.name::text,
            oh_1.dept_id_list || c.id::text AS text
           FROM ct_dept c
             JOIN dept_hierarchy oh_1 ON c.parent_id::text = oh_1.id::text
        )
 SELECT organization_id,
    id,
    name,
    code,
    enabled,
    category,
    parent_id,
    brief,
    source_category,
    source_id,
    seq,
    level,
    seq_list,
    name_list,
    dept_id_list,
        CASE
            WHEN (EXISTS ( SELECT 1
               FROM ct_dept child
              WHERE child.parent_id::text = oh.id::text)) THEN true
            ELSE false
        END AS has_child
   FROM dept_hierarchy oh
  ORDER BY seq_list;
ALTER TABLE "public"."view_dept_tree" OWNER TO "dev";

-- ----------------------------
-- View structure for view_menu_tree
-- ----------------------------
DROP VIEW IF EXISTS "public"."view_menu_tree";
CREATE VIEW "public"."view_menu_tree" AS  WITH RECURSIVE menu_tree AS (
         SELECT cm.id,
            cm.parent_id,
            cm.name,
            cm.code,
            cm.enabled,
            cm.url,
            cm.icon,
            cm.seq,
            cm.type,
            1 AS level,
            ARRAY[cm.seq] AS seq_list,
            ARRAY[cm.name::text] AS name_list,
            ARRAY[cm.id::text] AS id_list
           FROM ct_menu cm
          WHERE cm.parent_id IS NULL
        UNION ALL
         SELECT cmu.id,
            cmu.parent_id,
            cmu.name,
            cmu.code,
            cmu.enabled,
            cmu.url,
            cmu.icon,
            cmu.seq,
            cmu.type,
            mt.level + 1 AS level,
            mt.seq_list || cmu.seq,
            mt.name_list || cmu.name::text,
            mt.id_list || cmu.id::text
           FROM ct_menu cmu
             JOIN menu_tree mt ON cmu.parent_id::text = mt.id::text
        )
 SELECT id,
    parent_id,
    name,
    code,
    enabled,
    url,
    icon,
    seq,
    type,
    level,
    seq_list,
    name_list,
    id_list
   FROM menu_tree
  ORDER BY seq_list;
ALTER TABLE "public"."view_menu_tree" OWNER TO "dev";

-- ----------------------------
-- View structure for view_organization_tree
-- ----------------------------
DROP VIEW IF EXISTS "public"."view_organization_tree";
CREATE VIEW "public"."view_organization_tree" AS  WITH RECURSIVE organization_hierarchy AS (
         SELECT co.id,
            co.name,
            co.code,
            co.enabled,
            co.category,
            co.parent_id,
            co.address,
            co.seq,
            1 AS level,
            ARRAY[co.seq] AS seq_list,
            ARRAY[co.name::text] AS name_list,
            ARRAY[co.id::text] AS organization_id_list
           FROM ct_organization co
          WHERE co.parent_id IS NULL
        UNION ALL
         SELECT c.id,
            c.name,
            c.code,
            c.enabled,
            c.category,
            c.parent_id,
            c.address,
            c.seq,
            oh_1.level + 1 AS level,
            oh_1.seq_list || c.seq,
            oh_1.name_list || c.name::text,
            oh_1.organization_id_list || c.id::text AS text
           FROM ct_organization c
             JOIN organization_hierarchy oh_1 ON c.parent_id::text = oh_1.id::text
        )
 SELECT id,
    name,
    code,
    enabled,
    category,
    parent_id,
    address,
    seq,
    level,
    seq_list,
    name_list,
    organization_id_list,
        CASE
            WHEN (EXISTS ( SELECT 1
               FROM ct_organization child
              WHERE child.parent_id::text = oh.id::text)) THEN true
            ELSE false
        END AS has_child
   FROM organization_hierarchy oh
  ORDER BY seq_list;
ALTER TABLE "public"."view_organization_tree" OWNER TO "dev";

-- ----------------------------
-- View structure for view_permission
-- ----------------------------
DROP VIEW IF EXISTS "public"."view_permission";
CREATE VIEW "public"."view_permission" AS  WITH assign_list AS (
         SELECT cpa_1.grant_type,
            cpa_1.grant_object_id,
            cpa_1.grantee_type,
            cpa_1.grantee_object_id,
            cpa_1.permission_id,
            cpa_1.start_time,
            cpa_1.policy,
            cpa_1.end_time,
            cpa_1.id,
            cpa_1.created_at,
            cpa_1.updated_at,
            cpa_1.operator,
            cpa_1.operator_category,
            cpa_1.version,
            cpa_1."desc",
            COALESCE(
                CASE
                    WHEN cpa_1.grantee_type = 'ROLE'::enumpermissionassigngranteetype THEN cr.name
                    WHEN cpa_1.grantee_type = 'USER'::enumpermissionassigngranteetype THEN cu.name
                    ELSE NULL::character varying
                END, NULL::character varying) AS grantee_object_name,
            COALESCE(
                CASE
                    WHEN cpa_1.grantee_type = 'ROLE'::enumpermissionassigngranteetype THEN cr.code
                    ELSE NULL::character varying
                END, NULL::character varying) AS grantee_object_code,
            COALESCE(
                CASE
                    WHEN cpa_1.grant_type = 'MENU'::enumpermissionassigngranttype THEN cm.name
                    WHEN cpa_1.grant_type = 'BACKEND_API'::enumpermissionassigngranttype THEN cba_1.url
                    ELSE NULL::character varying
                END, NULL::character varying) AS grant_object_name,
            COALESCE(
                CASE
                    WHEN cpa_1.grant_type = 'BACKEND_API'::enumpermissionassigngranttype THEN cba_1.ignore_auth
                    ELSE NULL::boolean
                END, NULL::boolean) AS ignore_auth
           FROM ct_permission_assign cpa_1
             LEFT JOIN ct_role cr ON cpa_1.grantee_type = 'ROLE'::enumpermissionassigngranteetype AND cpa_1.grantee_object_id::text = cr.id::text
             LEFT JOIN ct_web_user cu ON cpa_1.grantee_type = 'USER'::enumpermissionassigngranteetype AND cpa_1.grantee_object_id::text = cu.id::text
             LEFT JOIN ct_menu cm ON cpa_1.grant_type = 'MENU'::enumpermissionassigngranttype AND cpa_1.grant_object_id::text = cm.id::text
             LEFT JOIN ct_backend_api cba_1 ON cpa_1.grant_type = 'BACKEND_API'::enumpermissionassigngranttype AND cpa_1.grant_object_id::text = cba_1.id::text
        )
 SELECT cp.name,
    cp.code,
    cp.resource_category,
    cp.resource_id,
    cp.enabled,
    cp.id,
    cp.created_at,
    cp.updated_at,
    cp.operator,
    cp.operator_category,
    cp.version,
    cp."desc",
    cba.ignore_auth,
    COALESCE(json_agg(cpa.* ORDER BY cpa.updated_at) FILTER (WHERE cpa.id IS NOT NULL), '[]'::json) AS assign_list
   FROM ct_permission cp
     LEFT JOIN ct_backend_api cba ON cp.resource_category = 'BACKEND_API'::enumresourcepermissioncategory AND cp.resource_id::text = cba.id::text
     LEFT JOIN assign_list cpa ON cpa.permission_id::text = cp.id::text
  GROUP BY cp.id, cba.ignore_auth
  ORDER BY cp.resource_category, cp.name;
ALTER TABLE "public"."view_permission" OWNER TO "dev";

-- ----------------------------
-- Indexes structure for table bt_quiz
-- ----------------------------
CREATE INDEX "idx_bt_quiz_code" ON "public"."bt_quiz" USING btree (
  "code" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "ix_bt_quiz_id" ON "public"."bt_quiz" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table bt_quiz
-- ----------------------------
ALTER TABLE "public"."bt_quiz" ADD CONSTRAINT "bt_quiz_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table bt_quiz_outcome
-- ----------------------------
CREATE INDEX "idx_bt_quiz_outcome_code" ON "public"."bt_quiz_outcome" USING btree (
  "code" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_bt_quiz_outcome_quiz_id" ON "public"."bt_quiz_outcome" USING btree (
  "quiz_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "ix_bt_quiz_outcome_id" ON "public"."bt_quiz_outcome" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table bt_quiz_outcome
-- ----------------------------
ALTER TABLE "public"."bt_quiz_outcome" ADD CONSTRAINT "bt_quiz_outcome_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table bt_quiz_question
-- ----------------------------
CREATE INDEX "idx_bt_quiz_question_quiz_id" ON "public"."bt_quiz_question" USING btree (
  "quiz_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "ix_bt_quiz_question_id" ON "public"."bt_quiz_question" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table bt_quiz_question
-- ----------------------------
ALTER TABLE "public"."bt_quiz_question" ADD CONSTRAINT "bt_quiz_question_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table bt_quiz_result
-- ----------------------------
CREATE INDEX "idx_bt_quiz_result_quiz_id" ON "public"."bt_quiz_result" USING btree (
  "quiz_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_bt_quiz_result_token_id" ON "public"."bt_quiz_result" USING btree (
  "token_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "ix_bt_quiz_result_id" ON "public"."bt_quiz_result" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table bt_quiz_result
-- ----------------------------
ALTER TABLE "public"."bt_quiz_result" ADD CONSTRAINT "bt_quiz_result_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table bt_quiz_token
-- ----------------------------
CREATE INDEX "idx_bt_quiz_token_batch_code" ON "public"."bt_quiz_token" USING btree (
  "batch_code" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "idx_bt_quiz_token_token" ON "public"."bt_quiz_token" USING btree (
  "token" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "ix_bt_quiz_token_id" ON "public"."bt_quiz_token" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table bt_quiz_token
-- ----------------------------
ALTER TABLE "public"."bt_quiz_token" ADD CONSTRAINT "bt_quiz_token_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table bt_quiz_token_log
-- ----------------------------
CREATE INDEX "idx_bt_quiz_token_log_batch_code" ON "public"."bt_quiz_token_log" USING btree (
  "batch_code" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_bt_quiz_token_log_created_at" ON "public"."bt_quiz_token_log" USING btree (
  "created_at" "pg_catalog"."timestamptz_ops" ASC NULLS LAST
);
CREATE INDEX "idx_bt_quiz_token_log_quiz_id" ON "public"."bt_quiz_token_log" USING btree (
  "quiz_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_bt_quiz_token_log_token_id" ON "public"."bt_quiz_token_log" USING btree (
  "token_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "ix_bt_quiz_token_log_id" ON "public"."bt_quiz_token_log" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table bt_quiz_token_log
-- ----------------------------
ALTER TABLE "public"."bt_quiz_token_log" ADD CONSTRAINT "bt_quiz_token_log_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table bt_quiz_token_quiz
-- ----------------------------
CREATE INDEX "idx_bt_quiz_token_quiz_quiz_id" ON "public"."bt_quiz_token_quiz" USING btree (
  "quiz_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_bt_quiz_token_quiz_token_id" ON "public"."bt_quiz_token_quiz" USING btree (
  "token_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "ix_bt_quiz_token_quiz_id" ON "public"."bt_quiz_token_quiz" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table bt_quiz_token_quiz
-- ----------------------------
ALTER TABLE "public"."bt_quiz_token_quiz" ADD CONSTRAINT "bt_quiz_token_quiz_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table ct_backend_api
-- ----------------------------
CREATE INDEX "idx_ct_backend_api_name" ON "public"."ct_backend_api" USING btree (
  "name" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_ct_backend_api_url" ON "public"."ct_backend_api" USING btree (
  "url" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "ix_ct_backend_api_id" ON "public"."ct_backend_api" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table ct_backend_api
-- ----------------------------
ALTER TABLE "public"."ct_backend_api" ADD CONSTRAINT "ct_backend_api_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table ct_config_dict
-- ----------------------------
CREATE INDEX "idx_ct_config_dict_code" ON "public"."ct_config_dict" USING btree (
  "code" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_ct_config_dict_name" ON "public"."ct_config_dict" USING btree (
  "name" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "ix_ct_config_dict_id" ON "public"."ct_config_dict" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table ct_config_dict
-- ----------------------------
ALTER TABLE "public"."ct_config_dict" ADD CONSTRAINT "ct_config_dict_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table ct_dept
-- ----------------------------
CREATE INDEX "idx_ct_dept_organization_id" ON "public"."ct_dept" USING btree (
  "organization_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_ct_dept_parent_id" ON "public"."ct_dept" USING btree (
  "parent_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "ix_ct_dept_id" ON "public"."ct_dept" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table ct_dept
-- ----------------------------
ALTER TABLE "public"."ct_dept" ADD CONSTRAINT "ct_dept_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table ct_file_info
-- ----------------------------
CREATE INDEX "idx_ct_file_info_file_storage_id" ON "public"."ct_file_info" USING btree (
  "file_storage_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "ix_ct_file_info_id" ON "public"."ct_file_info" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table ct_file_info
-- ----------------------------
ALTER TABLE "public"."ct_file_info" ADD CONSTRAINT "ct_file_info_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table ct_file_resource
-- ----------------------------
CREATE INDEX "idx_ct_file_resource_file_info_id" ON "public"."ct_file_resource" USING btree (
  "file_info_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_ct_file_resource_resource_id" ON "public"."ct_file_resource" USING btree (
  "resource_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "ix_ct_file_resource_id" ON "public"."ct_file_resource" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table ct_file_resource
-- ----------------------------
ALTER TABLE "public"."ct_file_resource" ADD CONSTRAINT "ct_file_resource_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table ct_file_storage
-- ----------------------------
CREATE INDEX "ix_ct_file_storage_id" ON "public"."ct_file_storage" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table ct_file_storage
-- ----------------------------
ALTER TABLE "public"."ct_file_storage" ADD CONSTRAINT "ct_file_storage_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table ct_invite_code
-- ----------------------------
CREATE INDEX "ix_ct_invite_code_id" ON "public"."ct_invite_code" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table ct_invite_code
-- ----------------------------
ALTER TABLE "public"."ct_invite_code" ADD CONSTRAINT "ct_invite_code_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table ct_menu
-- ----------------------------
CREATE INDEX "idx_ct_menu_parent_id" ON "public"."ct_menu" USING btree (
  "parent_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "ix_ct_menu_id" ON "public"."ct_menu" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table ct_menu
-- ----------------------------
ALTER TABLE "public"."ct_menu" ADD CONSTRAINT "ct_menu_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table ct_organization
-- ----------------------------
CREATE INDEX "idx_ct_organization_parent_id" ON "public"."ct_organization" USING btree (
  "parent_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "ix_ct_organization_id" ON "public"."ct_organization" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table ct_organization
-- ----------------------------
ALTER TABLE "public"."ct_organization" ADD CONSTRAINT "ct_organization_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table ct_permission
-- ----------------------------
CREATE INDEX "idx_ct_permission_code" ON "public"."ct_permission" USING btree (
  "code" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_ct_permission_resource_category" ON "public"."ct_permission" USING btree (
  "resource_category" "pg_catalog"."enum_ops" ASC NULLS LAST
);
CREATE INDEX "idx_ct_permission_resource_id" ON "public"."ct_permission" USING btree (
  "resource_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "ix_ct_permission_id" ON "public"."ct_permission" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table ct_permission
-- ----------------------------
ALTER TABLE "public"."ct_permission" ADD CONSTRAINT "ct_permission_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table ct_permission_assign
-- ----------------------------
CREATE INDEX "idx_ct_permission_assign_grant_object_id" ON "public"."ct_permission_assign" USING btree (
  "grant_object_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_ct_permission_assign_grantee_object_id" ON "public"."ct_permission_assign" USING btree (
  "grantee_object_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_ct_permission_assign_permission_id" ON "public"."ct_permission_assign" USING btree (
  "permission_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "ix_ct_permission_assign_id" ON "public"."ct_permission_assign" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table ct_permission_assign
-- ----------------------------
ALTER TABLE "public"."ct_permission_assign" ADD CONSTRAINT "ct_permission_assign_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table ct_robot
-- ----------------------------
CREATE INDEX "ix_ct_robot_id" ON "public"."ct_robot" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table ct_robot
-- ----------------------------
ALTER TABLE "public"."ct_robot" ADD CONSTRAINT "ct_robot_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table ct_role
-- ----------------------------
CREATE INDEX "ix_ct_role_id" ON "public"."ct_role" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table ct_role
-- ----------------------------
ALTER TABLE "public"."ct_role" ADD CONSTRAINT "ct_role_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table ct_transaction
-- ----------------------------
CREATE INDEX "ix_ct_transaction_id" ON "public"."ct_transaction" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table ct_transaction
-- ----------------------------
ALTER TABLE "public"."ct_transaction" ADD CONSTRAINT "ct_transaction_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table ct_transaction_log
-- ----------------------------
CREATE INDEX "ix_ct_transaction_log_id" ON "public"."ct_transaction_log" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table ct_transaction_log
-- ----------------------------
ALTER TABLE "public"."ct_transaction_log" ADD CONSTRAINT "ct_transaction_log_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table ct_union_user
-- ----------------------------
CREATE INDEX "idx_ct_union_user_name" ON "public"."ct_union_user" USING btree (
  "name" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "ix_ct_union_user_id" ON "public"."ct_union_user" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table ct_union_user
-- ----------------------------
ALTER TABLE "public"."ct_union_user" ADD CONSTRAINT "ct_union_user_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table ct_union_user_user
-- ----------------------------
CREATE INDEX "idx_ct_union_user_user_category_user_id" ON "public"."ct_union_user_user" USING btree (
  "union_user_user_category" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "union_user_user_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_ct_union_user_user_union_user_id" ON "public"."ct_union_user_user" USING btree (
  "union_user_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "ix_ct_union_user_user_id" ON "public"."ct_union_user_user" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table ct_union_user_user
-- ----------------------------
ALTER TABLE "public"."ct_union_user_user" ADD CONSTRAINT "ct_union_user_user_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table ct_user_role
-- ----------------------------
CREATE INDEX "idx_user_role" ON "public"."ct_user_role" USING btree (
  "user_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "role_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "ix_ct_user_role_id" ON "public"."ct_user_role" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table ct_user_role
-- ----------------------------
ALTER TABLE "public"."ct_user_role" ADD CONSTRAINT "ct_user_role_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table ct_web_user
-- ----------------------------
CREATE INDEX "ix_ct_web_user_id" ON "public"."ct_web_user" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table ct_web_user
-- ----------------------------
ALTER TABLE "public"."ct_web_user" ADD CONSTRAINT "ct_web_user_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table ct_web_user_dept
-- ----------------------------
CREATE INDEX "ix_ct_web_user_dept_id" ON "public"."ct_web_user_dept" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table ct_web_user_dept
-- ----------------------------
ALTER TABLE "public"."ct_web_user_dept" ADD CONSTRAINT "ct_web_user_dept_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table ct_web_user_organization
-- ----------------------------
CREATE INDEX "ix_ct_web_user_organization_id" ON "public"."ct_web_user_organization" USING btree (
  "id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table ct_web_user_organization
-- ----------------------------
ALTER TABLE "public"."ct_web_user_organization" ADD CONSTRAINT "ct_web_user_organization_pkey" PRIMARY KEY ("id");
