from sqlalchemy import Column, String, Index
from basic.entity.basic_entity import BasicEntity


class QuizTokenQuizEntity(BasicEntity):
    """Token 授权测验关联表

    记录某个 token 被限定可访问的测验。
    若 bt_quiz_token 在此表无任何记录，则该 token 可访问所有已发布测验。
    """
    __tablename__ = 'bt_quiz_token_quiz'
    __table_args__ = (
        Index('idx_bt_quiz_token_quiz_token_id', 'token_id'),
        Index('idx_bt_quiz_token_quiz_quiz_id', 'quiz_id'),
        {"comment": "Token 授权测验关联表"}
    )

    token_id = Column(String(40), nullable=False, comment='关联的 token ID')
    quiz_id = Column(String(40), nullable=False, comment='授权的测验 ID')
