from sqlalchemy import Column, String

from basic.entity.basic_entity import BasicEntity


class WebUserOrganizationEntity(BasicEntity):
    __tablename__ = 'ct_web_user_organization'
    __table_args__ = (
        {"comment": "web用户所属组织表"}
    )

    web_user_id = Column(String(40), nullable=True, comment='web用户ID')
    organization_id = Column(String(40), nullable=True, comment='组织ID')
