from sqlalchemy import Column, String, Integer, Index, DateTime
from sqlalchemy.dialects.postgresql import JSONB

from basic.entity.basic_entity import BasicEntity


class QuizTokenEntity(BasicEntity):
    """测验访问令牌表

    一个 token 可用于参加所有已发布测验，使用次数由 max_uses 控制。
    NULL max_uses 表示不限次数。
    """
    __tablename__ = 'bt_quiz_token'
    __table_args__ = (
        Index('idx_bt_quiz_token_token', 'token', unique=True),
        Index('idx_bt_quiz_token_batch_code', 'batch_code'),
        {"comment": "测验访问令牌表"}
    )

    token = Column(String(64), nullable=False, comment='访问令牌（随机字符串），用于链接中的唯一标识')
    # active=可用 | exhausted=次数已耗尽 | expired=已过期
    status = Column(String(20), nullable=False, server_default='active', comment='状态：active/exhausted/expired')
    max_uses = Column(Integer, nullable=True, comment='最大使用次数，NULL表示不限次数')
    used_count = Column(Integer, nullable=False, server_default='0', comment='已使用次数')
    # purchase=购买 | gift=赠送 | admin=后台发放 | batch=批量生成
    source = Column(String(20), nullable=False, server_default='admin', comment='令牌来源：purchase/gift/admin/batch')
    batch_code = Column(String(100), nullable=True, comment='批次编码，批量生成时使用，便于管理')
    expires_at = Column(DateTime(timezone=True), nullable=True, comment='过期时间，NULL表示永不过期')
    extra = Column(JSONB, nullable=True, comment='扩展信息 JSON，如购买订单号、赠送备注等')
