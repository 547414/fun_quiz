from sqlalchemy import Column, String
from basic.entity.basic_entity import BasicEntity


class WebUserDeptEntity(BasicEntity):
    __tablename__ = 'ct_web_user_dept'
    __table_args__ = (
        {"comment": "web用户所属部门表"}
    )

    web_user_id = Column(String(40), nullable=True, comment='web用户ID')
    dept_id = Column(String(40), nullable=True, comment='部门ID')
