from sqlalchemy import Column, String, Index

from basic.entity.basic_entity import BasicEntity


class FileInfoEntity(BasicEntity):
    __tablename__ = 'ct_file_info'
    __table_args__ = (
        Index('idx_ct_file_info_file_storage_id', 'file_storage_id'),
        {"comment": "文件信息表"}
    )

    name = Column(String(255), nullable=False, comment='文件名')
    file_storage_id = Column(String(40), nullable=False, comment='文件存储ID')
