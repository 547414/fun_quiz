import axios from '@/utils/request';
import {Response} from "@/utils/requestTypes.ts";

const prefix = '/permission';

export interface PermissionPageParams {
    pageSize: number;
    pageIndex: number;
    categoryList: string[] | null;
    search: string | null;
    nameSort: string | null;
    searchFields: string[];
}


export interface PermissionPageResponse extends Response {
    data: {
        filterCount: number;
        pageIndex: number;
        pageSize: number;
        totalCount: number;
        data: PermissionPageDetail[];
    }
}

export interface PermissionPageDetail {
    id: string;
    name: string;
    code: string;
    enabled: boolean;
    resourceCategory: string;
    resourceId: string;
    resourceCategoryDisplay: string | null;
    assignList: PermissionAssign[] | null;
    ignoreAuth: boolean | null;
}

export const apiGetPermissionPage = (params: PermissionPageParams): Promise<PermissionPageResponse> => {
    return axios.post(`${prefix}/page`, params);
};

export interface PermissionDetailResponse extends Response {
    data: PermissionDetail;
}

export interface PermissionAssign {
    id: string;
    grantType: string;
    grantObjectId: string;
    granteeType: string;
    granteeObjectId: string;
    grantObjectName: string | null;
    granteeObjectName: string | null;
    granteeObjectCode: string | null;
    permissionId: string | null;
    startTime: Date;
    endTime: Date | null;
    policy: string;
    ignoreAuth: boolean | null;
}

export interface assignName {
    grantType: string;
    nameList: string[] | null;
}

export interface PermissionDetail {
    id: string;
    name: string;
    code: string;
    resourceCategory: string;
    resourceId: string;
    enabled: boolean;
    assignList: PermissionAssign[] | null;
    assignNameList: assignName[] | null;
    ignoreAuth: boolean | null;
}

export const apiGetPermissionDetail = (permissionId: string): Promise<PermissionDetailResponse> => {
    return axios.get(`${prefix}/detail/${permissionId}`);
};

export const apiEditPermission = (params: PermissionDetail): Promise<Response> => {
    return axios.post(`${prefix}/edit`, params);
};

export interface ChangePermissionEnabledParams {
    id: string;
    enabled: boolean;
}

export const apiChangePermissionEnabled = (params: ChangePermissionEnabledParams): Promise<Response> => {
    return axios.post(`${prefix}/change_enabled`, params);
};


export interface DeletePermissionParams {
    permissionId: string;
}

export const apiDeletePermission = (params: DeletePermissionParams): Promise<Response> => {
    return axios.post(`${prefix}/delete`, params);
};