from sqlalchemy import Column, String, Boolean, Integer, Index
from sqlalchemy.dialects.postgresql import JSONB

from basic.entity.basic_entity import BasicEntity


class QuizEntity(BasicEntity):
    """测验主表"""
    __tablename__ = 'bt_quiz'
    __table_args__ = (
        Index('idx_bt_quiz_code', 'code'),
        {"comment": "测验主表"}
    )

    name = Column(String(200), nullable=False, comment='测验名称')
    code = Column(String(100), nullable=False, comment='测验编码，唯一标识')
    # [{file_info_id, file_name, url, bucket_name, object_name, ...}]
    covers = Column(JSONB, nullable=True, comment='封面图文件列表 JSON Array')
    # {prompt, style, negative_prompt}
    cover_prompt = Column(JSONB, nullable=True, comment='封面图生成提示词配置 JSON')
    # vector=多维向量匹配(SBTI/MBTI) | score=累分段映射 | branch=分支跳题 | random=加权随机
    quiz_type = Column(String(40), nullable=False, server_default='vector', comment='测验类型')
    # draft=草稿(AI生成待审核) | published=已发布 | archived=已归档
    status = Column(String(20), nullable=False, server_default='draft', comment='状态：draft/published/archived')
    # manual=手动创建 | ai=AI生成导入
    source = Column(String(20), nullable=False, server_default='manual', comment='创建来源：manual/ai')
    sort_order = Column(Integer, nullable=False, server_default='0', comment='排序')
    share_title = Column(String(200), nullable=True, comment='分享标题')
    share_desc = Column(String(500), nullable=True, comment='分享描述')
    fallback_outcome_code = Column(String(100), nullable=True, comment='兜底结果编码（匹配度不足时使用）')
    algo_config = Column(JSONB, nullable=True, comment='算法配置 JSON，结构随 quiz_type 变化（详见 doc/SKILL.md）')
    special_rules = Column(JSONB, nullable=True, comment='特殊判定规则 JSON（详见 doc/SKILL.md）')
    result_config = Column(JSONB, nullable=True, comment='结果页展示配置 JSON（详见 doc/SKILL.md）')
