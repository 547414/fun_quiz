import axios from '@/utils/request';
import {Response} from "@/utils/requestTypes.ts";

const prefix = '/storage';

export interface UploadParams {
    file: File;
    fileName: string | null;
    fileSize: number | null;
}

export interface UploadResponseParams extends Response {
    data: {
        fileInfoId: string,
        fileName: string | null,
        fileType: string | null,
        fileSize: number | null,
        bucketName: string,
        objectName: string,
        fileObjectName: string,
        url: string,
        type: string | null
    }
}

export const apiUploadFile = (params: UploadParams): Promise<UploadResponseParams> => {
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

export interface UploadBase64Params {
    file: string;
    fileName: string | null;
    fileSize: number | null;
}

export const apiUploadBase64File = (params: UploadBase64Params): Promise<UploadResponseParams> => {
    return axios.post(`${prefix}/upload_base64`, params);
};


export interface WwUploadParams {
    serverId: string;
}

export const apiWwUploadFile = (params: WwUploadParams): Promise<UploadResponseParams> => {
    return axios.post(`/ww/upload`, params);
};


export interface GetFileInfoParams {
    fileInfoIdList: string[];
}

export interface FileInfoListResponse extends Response {
    data: FileInfoListDetail[]
}

export interface FileInfoListDetail {
    fileInfoId: string,
    fileName: string | null,
    fileType: string | null,
    fileSize: number | null,
    bucketName: string,
    objectName: string,
    fileObjectName: string,
    url: string,
    type: string | null
}

export const apiGetFileInfoList = (params: GetFileInfoParams): Promise<FileInfoListResponse> => {
    return axios.post(`${prefix}/file_info_list`, params);
};
