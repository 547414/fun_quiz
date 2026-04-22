from sqlalchemy import Column, String, Integer, Index
from sqlalchemy.dialects.postgresql import JSONB

from basic.entity.basic_entity import BasicEntity


class QuizResultEntity(BasicEntity):
    """用户答题结果记录表"""
    __tablename__ = 'bt_quiz_result'
    __table_args__ = (
        Index('idx_bt_quiz_result_token_id', 'token_id'),
        Index('idx_bt_quiz_result_quiz_id', 'quiz_id'),
        {"comment": "用户答题结果记录表"}
    )

    token_id = Column(String(40), nullable=False, comment='关联的访问令牌ID（唯一，一个token只能产生一条结果）')
    quiz_id = Column(String(40), nullable=False, comment='所属测验ID')
    answers = Column(JSONB, nullable=False, comment='原始答案 JSON，格式：{question_seq: option_key}')
    # 中间计算产物，结构随 quiz_type 变化：
    #   vector: {dim_scores:{dim_code:raw_score}, dim_vector:[1,2,3,...]}
    #   score:  {total_score: 42}
    #   branch: {path:[1,3,5,...]}
    #   random: {}
    calc_result = Column(JSONB, nullable=True, comment='计算中间结果 JSON，结构随 quiz_type 变化')
    outcome_code = Column(String(100), nullable=False, comment='命中结果编码')
    outcome_id = Column(String(40), nullable=False, comment='命中结果ID')
    score = Column(Integer, nullable=True, comment='匹配度（百分比），vector/score类型有值，其他为NULL')
    # {bucket, key, url, size, mime_type}，异步生成后回填
    share_image = Column(JSONB, nullable=True, comment='分享图文件 JSON')
