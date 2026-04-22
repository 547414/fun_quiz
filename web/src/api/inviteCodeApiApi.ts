import axios from '@/utils/request';
import {Response} from "@/utils/requestTypes.ts";

const prefix = '/invite_code';


export interface InviteCodePageParams {
    pageSize: number;
    pageIndex: number;
    search: string | null;
    searchFields: string[];
    nameSort: string;
}


export interface InviteCodePageResponse extends Response {
    data: {
        filterCount: number;
        pageIndex: number;
        pageSize: number;
        totalCount: number;
        data: InviteCodeDetail[];
    }
}

export interface InviteCodeDetail {
    id: string;
    code: string | null;
    brief: string | null;
    maxLimit: number | null;
    registerNum: number | null;
    deadline: Date | null;
    enabled: boolean;
    deleted: boolean;
}

export const apiGetInviteCodePage = (params: InviteCodePageParams): Promise<InviteCodePageResponse> => {
    return axios.post(`${prefix}/page`, params);
};

export interface EditInviteCodeParams {
    id: string;
    code: string | null;
    brief: string | null;
    maxLimit: number | null;
    registerNum: number | null;
    deadline: Date | null;
    enabled: boolean;
    deleted: boolean;
}

export const apiEditInviteCode = (params: EditInviteCodeParams): Promise<Response> => {
    return axios.post(`${prefix}/edit`, params);
};

export interface DeleteInviteCodeParams {
    inviteCodeId: string;
}

export const apiDeleteInviteCode = (params: DeleteInviteCodeParams): Promise<Response> => {
    return axios.post(`${prefix}/soft_delete`, params);
};

export interface ChangeInviteCodeEnableParams {
    inviteCodeId: string;
    enabled: boolean;
}

export const apiChangeInviteCodeEnabled = (params: ChangeInviteCodeEnableParams): Promise<Response> => {
    return axios.post(`${prefix}/change_enabled`, params);
};

export interface InviteCodeDetailResponse extends Response {
    data: EditInviteCodeParams
}

export const apiGetInviteCodeDetail = (inviteCodeId: string): Promise<InviteCodeDetailResponse> => {
    return axios.get(`${prefix}/detail/${inviteCodeId}`);
};

export interface InviteCodeStatistics {
    total: number;
    runOut: number;
    notRunOut: number;
    expired: number;
}

export interface InviteCodeStatisticsResponse extends Response {
    data: InviteCodeStatistics
}

export const apiGetInviteCodeStatistics = (): Promise<InviteCodeStatisticsResponse> => {
    return axios.get(`${prefix}/statistics`);
};
