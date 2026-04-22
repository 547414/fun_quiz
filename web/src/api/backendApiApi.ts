import axios from '@/utils/request';
import {Response} from "@/utils/requestTypes.ts";

const prefix = '/backend_api';


export interface BackendApiPageParams {
    pageSize: number;
    pageIndex: number;
    search: string | null;
    searchFields: string[];
}


export interface BackendApiPageResponse extends Response {
    data: {
        filterCount: number;
        pageIndex: number;
        pageSize: number;
        totalCount: number;
        data: BackendApiDetail[];
    }
}

export interface BackendApiDetail {
    id: string;
    name: string | null;
    code: string | null;
    enabled: boolean;
    url: string;
    ignore_auth: boolean;
}

export interface ChangeBackendApiIgnoreAuthParams {
    id: string;
    ignoreAuth: boolean;
}

export const apiGetBackendApiPage = (params: BackendApiPageParams): Promise<BackendApiPageResponse> => {
    return axios.post(`${prefix}/page`, params);
};

export const apiChangeBackendApiIgnoreAuth = (params: ChangeBackendApiIgnoreAuthParams): Promise<Response> => {
    return axios.post(`${prefix}/change_ignore_auth`, params);
};
