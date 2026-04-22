from sqlalchemy import Column, String, Integer, Boolean, Index
from sqlalchemy.dialects.postgresql import JSONB

from basic.entity.basic_entity import BasicEntity


class QuizQuestionEntity(BasicEntity):
    """测验题目表"""
    __tablename__ = 'bt_quiz_question'
    __table_args__ = (
        Index('idx_bt_quiz_question_quiz_id', 'quiz_id'),
        {"comment": "测验题目表"}
    )

    quiz_id = Column(String(40), nullable=False, comment='所属测验ID')
    seq = Column(Integer, nullable=False, comment='题目序号，从1开始，branch类型用于跳转引用')
    content = Column(String(1000), nullable=False, comment='题目内容')
    # [{file_info_id, file_name, url, bucket_name, object_name, ...}]
    images = Column(JSONB, nullable=True, comment='题目配图文件列表 JSON Array')
    # {prompt, style, negative_prompt}
    image_prompt = Column(JSONB, nullable=True, comment='题目图片生成提示词配置 JSON')
    is_hidden = Column(Boolean, nullable=False, server_default='false', comment='是否隐藏判定题（配合 special_rules 触发特殊结果）')
    # options JSON 结构随 quiz_type 变化（详见 doc/SKILL.md questions 章节）：
    #   vector: [{key, label, dim_scores: {dim_code: 1|2|3}}]
    #   score:  [{key, label, score: int}]
    #   branch: [{key, label, next_question_seq: int, outcome_code?: str}]
    #   random: [{key, label}]
    options = Column(JSONB, nullable=False, comment='选项配置 JSON，结构随 quiz_type 变化')
    # branch 类型专用：{default_next_seq: int}
    branch_config = Column(JSONB, nullable=True, comment='分支跳题配置 JSON，仅 branch 类型使用')
