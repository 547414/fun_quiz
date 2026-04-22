from sqlalchemy import Column, String, Integer, Boolean, Index
from sqlalchemy.dialects.postgresql import JSONB

from basic.entity.basic_entity import BasicEntity


class QuizOutcomeEntity(BasicEntity):
    """测验结果模板表（通用，适配所有测验类型）"""
    __tablename__ = 'bt_quiz_outcome'
    __table_args__ = (
        Index('idx_bt_quiz_outcome_quiz_id', 'quiz_id'),
        Index('idx_bt_quiz_outcome_code', 'code'),
        {"comment": "测验结果模板表"}
    )

    quiz_id = Column(String(40), nullable=False, comment='所属测验ID')
    code = Column(String(100), nullable=False, comment='结果编码，同一测验内唯一，如 ATM-er / INTJ / LATTE')
    name = Column(String(200), nullable=False, comment='结果名称')
    avatar = Column(JSONB, nullable=True, comment='结果形象图文件 JSON')
    # {prompt, style, negative_prompt}
    avatar_prompt = Column(JSONB, nullable=True, comment='结果头像生成提示词配置 JSON')
    summary = Column(String(500), nullable=True, comment='结果简短描述（结果页副标题）')
    detail = Column(String, nullable=True, comment='结果详细解读文案（支持富文本）')
    tags = Column(JSONB, nullable=True, comment='特征标签 JSON，如 ["高付出","社交边界低"]')
    sort_order = Column(Integer, nullable=False, server_default='0', comment='排序')
    is_fallback = Column(Boolean, nullable=False, server_default='false', comment='是否为兜底结果')
    is_special = Column(Boolean, nullable=False, server_default='false', comment='是否为特殊触发结果（由 special_rules 命中）')
    # 匹配条件，结构随 quiz_type 变化（详见 doc/SKILL.md outcomes 章节）：
    #   vector: {dim_vector: [1|2|3, ...]}
    #   score:  {score_min: int, score_max: int}
    #   branch: {}
    #   random: {weight: int}
    match_config = Column(JSONB, nullable=True, comment='匹配条件 JSON，结构随 quiz_type 变化')
