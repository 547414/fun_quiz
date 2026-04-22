import axios from '@/utils/request';
import {Response} from "@/utils/requestTypes.ts";

const prefix = '/storage';

export interface UploadFileInfo {
    fileInfoId?: string | null
    fileName?: string | null
    fileType?: string | null
    fileSize?: number | null
    bucketName?: string
    objectName?: string
    fileObjectName?: string | null
    url?: string | null
    fileHash?: string | null
}

export interface UploadParams {
    file: File;
    fileName: string | null;
    fileSize: number | null;
}

export interface FileDetail {
    fileInfoId: string | null,
    fileName: string | null,
    fileType: string | null,
    fileSize: number | null,
    bucketName: string,
    objectName: string,
    fileObjectName: string | null,
    url: string | null,
    type: string | null
}

export interface UploadResponse extends Response {
    data: FileDetail
}

export const apiUploadFile = (params: UploadParams): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('file', params.file); // 如果有文件需要上传
    if (params.fileName) {
        formData.append('file_name', params.fileName);
    }
    if (params.fileSize) {
        formData.append('file_size', params.fileSize.toString());
    }
    return axios.post(`${prefix}/upload`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
};


export const apiGetFileUrl = (fileInfoId: string): Promise<Response> => {
    return axios.get(`${prefix}/file_url/${fileInfoId}`);
};
