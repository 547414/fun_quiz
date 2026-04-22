import axios from '@/utils/request';
import {Response} from "@/utils/requestTypes.ts";

const prefix = '/role';


export interface RolePageParams {
    pageSize: number;
    pageIndex: number;
    search: string | null;
    searchFields: string[];
}


export interface RolePageResponse extends Response {
    data: {
        filterCount: number;
        pageIndex: number;
        pageSize: number;
        totalCount: number;
        data: RoleDetail[];
    }
}

export interface RoleDetail {
    id: string;
    brief: string | null;
    name: string;
    code: string;
    enabled: boolean;
    createdAt: Date | null;
    updatedAt: Date | null;
}

export const apiGetRolePage = (params: RolePageParams): Promise<RolePageResponse> => {
    return axios.post(`${prefix}/page`, params);
};


export interface ChangeRoleEnabledParams {
    id: string;
    enabled: boolean;
}

export const apiChangeRoleEnabled = (params: ChangeRoleEnabledParams): Promise<Response> => {
    return axios.post(`${prefix}/change_enabled`, params);
};


export const apiEditRole = (params: RoleDetail): Promise<Response> => {
    return axios.post(`${prefix}/edit`, params);
};

export interface DeleteRoleParams {
    roleId: string;
}

export const apiDeleteRole = (params: DeleteRoleParams): Promise<Response> => {
    return axios.post(`${prefix}/delete`, params);
};

export interface RoleStatistics {
    total: number;
    enabledCount: number;
    disableCount: number;
    newestUpdatedAt: number;
}

export interface RoleStatisticsResponse extends Response {
    data: RoleStatistics
}

export const apiGetRoleStatistics = (): Promise<RoleStatisticsResponse> => {
    return axios.get(`${prefix}/statistics`);
};
