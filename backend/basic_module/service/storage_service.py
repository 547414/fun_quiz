import base64
import hashlib
import io
import os
import uuid
import zipfile
from typing import Optional

import magic
import toml

from basic.minio_client.minio_client import MinioClient
from basic_module.entity.file_resource import FileResourceEntity
from basic_module.model.file_info_model import FileInfoModel, FileInfoListParams
from basic_module.model.file_resource_model import FileResourceModel
from basic_module.model.file_storage_model import FileStorageModel
from basic_module.model.upload_model import UploadBase64Params, UploadResModel
from basic_module.repository.file_info_repository import FileInfoRepository
from basic_module.repository.file_resource_repository import FileResourceRepository
from basic_module.repository.file_storage_repository import FileStorageRepository


class StorageService:

    def __init__(
            self,
            minio_client: MinioClient,
            file_info_repository: FileInfoRepository,
            file_storage_repository: FileStorageRepository,
            file_resource_repository: FileResourceRepository,
    ):
        self.__minio_client = minio_client
        self.__file_info_repository = file_info_repository
        self.__file_storage_repository = file_storage_repository
        self.__file_resource_repository = file_resource_repository
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.__base_path = os.path.join(path, "../")
        self.__app_config = toml.load(fr"{self.__base_path}/app_config.toml")
        self.__active = self.__app_config.get('settings', {}).get('active', 'development')
        self.__config_name = f'app_{self.__active}_config.toml'
        self.__config = toml.load(fr"{self.__base_path}/config/{self.__config_name}")

    @staticmethod
    def detect_file_type(file, file_name: str = None):
        try:
            file.seek(0)
            with zipfile.ZipFile(file) as zf:
                namelist = zf.namelist()
                if 'word/document.xml' in namelist:
                    return "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                elif 'xl/workbook.xml' in namelist:
                    return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                elif 'ppt/presentation.xml' in namelist:
                    return "application/vnd.openxmlformats-officedocument.presentationml.presentation"
                else:
                    if file_name:
                        ext = file_name.lower().split('.')[-1]
                        if ext == 'doc':
                            return "application/msword"
                        elif ext == 'xls':
                            return "application/vnd.ms-excel"
                        elif ext == 'ppt':
                            return "application/vnd.ms-powerpoint"
                    else:
                        return "application/zip"
        except zipfile.BadZipFile:
            # 不可解压为zip，尝试识别旧Office格式
            file.seek(0)
            mime = magic.Magic(mime=True)
            mime_type = mime.from_buffer(file.read(2048))

            # 进一步判断是否为旧版 Office 文件
            if mime_type == "application/msword":
                return "application/msword"  # .doc
            elif mime_type == "application/vnd.ms-excel":
                return "application/vnd.ms-excel"  # .xls
            elif mime_type == "application/vnd.ms-powerpoint":
                return "application/vnd.ms-powerpoint"  # .ppt
            elif mime_type in ("application/CDFV2", "application/octet-stream"):
                # 如果是通用复合文档格式，再结合扩展名判断
                if file_name:
                    ext = file_name.lower().split('.')[-1]
                    if ext == 'doc':
                        return "application/msword"
                    elif ext == 'xls':
                        return "application/vnd.ms-excel"
                    elif ext == 'ppt':
                        return "application/vnd.ms-powerpoint"
                return "application/CDFV2"  # 无法确认具体类型
            else:
                return mime_type
        finally:
            file.seek(0)  # 重置指针

    def upload(
            self,
            file,
            file_name: Optional[str] = None,
            file_size: Optional[int] = None,
            bucket_path: Optional[str] = None
    ):
        file.seek(0, 2)
        real_file_size = file.tell()
        file.seek(0)
        if file_size is None:
            file_size = real_file_size
        # max_file_size单位是MB
        max_file_size = int(self.__config.get('storage', {}).get('max_file_size', 10))
        if real_file_size > max_file_size * 1024 * 1024:
            raise Exception(f"文件大小超过{max_file_size}MB")
        # 计算文件hash
        hasher = hashlib.sha256()
        for chunk in file:
            hasher.update(chunk)
        file_hash = hasher.hexdigest()
        file.seek(0)  # 重置文件指针确保上传时读取完整文件
        # 判断文件是否已上传过
        exist_file_storage = self.__file_storage_repository.get_exist(
            file_hash=file_hash
        )

        # 推断文件类型
        # mime = magic.Magic(mime=True)
        # file.seek(0)  # 确保在读取 MIME 类型前，重置指针
        # file_type = mime.from_buffer(file.read(1024))
        # file.seek(0)

        file_type = self.detect_file_type(file=file, file_name=file_name)

        if not file_name:
            file_name = f"{file_hash[:8]}.{file_type.split('/')[1]}"

        if not exist_file_storage:
            # 上传文件到minio
            bucket_name, bucket_path, object_name, file_object_name = self.__minio_client.put_object(
                data=io.BytesIO(file.read()),
                file_name=file_name,
                bucket_path=bucket_path
            )

            # 存入ct_file_storage
            file_storage_id = str(uuid.uuid4())
            file_storage_model = FileStorageModel(
                id=file_storage_id,
                original_name=file_name,
                object_name=file_object_name,
                bucket_name=bucket_name,
                path=bucket_path,
                endpoint=os.getenv("MINIO_ENDPOINT"),
                size=file_size,
                type=file_type,
                hash=file_hash
            )
            self.__file_storage_repository.insert(
                model=file_storage_model
            )
        else:
            file_storage_id = exist_file_storage.id
            bucket_name = exist_file_storage.bucket_name
            object_name = f"{exist_file_storage.path}/{exist_file_storage.object_name}"
            file_object_name = exist_file_storage.object_name
        # 存入ct_file_info
        file_info_id = str(uuid.uuid4())
        file_info_model = FileInfoModel(
            id=file_info_id,
            name=file_name,
            file_storage_id=file_storage_id
        )
        self.__file_info_repository.insert(
            model=file_info_model
        )
        # 获取预签名url
        url = self.__minio_client.get_file_url(
            bucket_name=bucket_name,
            object_name=object_name
        )
        return UploadResModel(
            file_info_id=file_info_id,
            file_name=file_name,
            file_type=file_type,
            file_size=file_size,
            file_hash=file_hash,
            bucket_name=bucket_name,
            object_name=object_name,
            file_object_name=file_object_name,
            url=url
        )

    def upload_base64(self, params: UploadBase64Params):
        base64_data = params.file  # Base64 编码的文件数据
        file_name = params.file_name
        file_data = base64.b64decode(base64_data)
        file_stream = io.BytesIO(file_data)
        return self.upload(
            file=file_stream,
            file_name=file_name,
            file_size=params.file_size
        )

    def get_file_info_list(self, params: FileInfoListParams):
        file_info_list = self.__file_info_repository.get_by_ids(
            ids=params.file_info_id_list
        )
        for file_info in file_info_list:
            file_info.url = self.__minio_client.get_file_url(
                bucket_name=file_info.bucket_name,
                object_name=file_info.object_name
            )
        return file_info_list

    def save_file_resource(self, file_resource: FileResourceModel):
        self.__file_resource_repository.insert(
            model=file_resource
        )

    def delete_file_resource(
            self,
            resource_category: str,
            resource_id: str,
            relationship: str,
    ):
        file_resource_list = self.__file_resource_repository.get_exist(
            resource_category=resource_category,
            resource_id=resource_id,
            relationship=relationship
        )
        if file_resource_list:
            for file_resource in file_resource_list:
                self.__file_resource_repository.delete(
                    entity_id=file_resource.id,
                    entity=FileResourceEntity,
                )

    def get_file_url(self, file_info_id: str):
        file_info = self.__file_info_repository.get_by_id(
            file_info_id=file_info_id
        )
        if not file_info:
            return None
        return self.__minio_client.get_file_url(
            bucket_name=file_info.bucket_name,
            object_name=f"{file_info.object_name}"
        )
