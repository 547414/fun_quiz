from sqlalchemy import Column, String, Index, Boolean
from sqlalchemy.dialects.postgresql import JSONB

from basic.entity.basic_entity import BasicEntity


class ConfigDictEntity(BasicEntity):
    __tablename__ = 'ct_config_dict'
    __table_args__ = (
        Index('idx_ct_config_dict_name', 'name'),
        Index('idx_ct_config_dict_code', 'code'),
        {"comment": "配置字段表"}
    )

    name = Column(String(255), nullable=True, comment='名称')
    code = Column(String(255), nullable=True, comment='编码')
    data = Column(JSONB, nullable=True, comment='配置数据')
    enabled = Column(Boolean, nullable=False, server_default='true', comment='是否启用')
