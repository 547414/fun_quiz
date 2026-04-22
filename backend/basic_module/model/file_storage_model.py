from pydantic import Field

from basic.model.basic_model import BasicVersionModel


class FileStorageModel(BasicVersionModel):
    original_name: str = Field(..., description="原始文件名")
    object_name: str = Field(..., description="存储对象名称")
    bucket_name: str = Field(..., description="存储桶名称")
    path: str = Field(..., description="存储路径")
    endpoint: str = Field(..., description="存储端点")
    size: int = Field(..., description="文件大小")
    type: str = Field(..., description="文件类型")
    hash: str = Field(..., description="文件哈希值")
