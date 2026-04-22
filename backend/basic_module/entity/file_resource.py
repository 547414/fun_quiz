from sqlalchemy import Column, String, Index

from basic.entity.basic_entity import BasicEntity


class FileResourceEntity(BasicEntity):
    __tablename__ = 'ct_file_resource'
    __table_args__ = (
        Index('idx_ct_file_resource_file_info_id', 'file_info_id'),
        Index('idx_ct_file_resource_resource_id', 'resource_id'),
        {"comment": "文件资源关系表"}
    )

    file_info_id = Column(String(40), nullable=False, comment='文件信息ID')
    resource_category = Column(String(255), nullable=False, comment='资源类型')
    resource_id = Column(String(40), nullable=False, comment='资源ID')
    relationship = Column(String(255), nullable=False, comment='关系')
