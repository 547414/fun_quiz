from sqlalchemy import Column, String, Integer, Index

from basic.entity.basic_entity import BasicEntity


class FileStorageEntity(BasicEntity):
    __tablename__ = 'ct_file_storage'
    __table_args__ = (
        {"comment": "文件存储表"}
    )

    original_name = Column(String(255), nullable=False, comment='原文件名')
    object_name = Column(String(255), nullable=False, comment='对象名')
    bucket_name = Column(String(255), nullable=False, comment='桶名')
    path = Column(String(255), nullable=False, comment='路径')
    endpoint = Column(String(255), nullable=False, comment='端点')
    size = Column(Integer, nullable=False, comment='文件大小')
    type = Column(String(255), nullable=False, comment='文件类型')
    hash = Column(String(255), nullable=False, comment='文件哈希')
