from sqlalchemy import Column, String, Boolean, Index

from basic.entity.basic_entity import BasicEntity


class BackendApiEntity(BasicEntity):
    __tablename__ = 'ct_backend_api'
    __table_args__ = (
        Index('idx_ct_backend_api_name', 'name'),
        Index('idx_ct_backend_api_url', 'url'),
        {"comment": "后端接口表"}
    )

    name = Column(String(500), nullable=True, comment='名称')
    code = Column(String(500), nullable=True, comment='编码')
    enabled = Column(Boolean, nullable=False, server_default='true', comment='是否启用')
    url = Column(String(500), nullable=False, comment='URL')
    ignore_auth = Column(Boolean, nullable=False, server_default='false', comment='是否忽略权限')
