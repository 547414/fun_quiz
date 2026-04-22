from sqlalchemy import Column, String, Index

from basic.entity.basic_entity import BasicEntity


class UnionUserUserEntity(BasicEntity):
    __tablename__ = 'ct_union_user_user'
    __table_args__ = (
        Index('idx_ct_union_user_user_union_user_id', 'union_user_id'),
        Index('idx_ct_union_user_user_category_user_id', 'union_user_user_category', 'union_user_user_id'),
        {"comment": "联合用户用户表"}
    )

    union_user_id = Column(String(40), nullable=True, comment='联合用户id')
    union_user_user_category = Column(String(255), nullable=True, comment='用户类别, 企微用户、微信小程序用户、web用户等')
    union_user_user_id = Column(String(40), nullable=True, comment='用户id')
