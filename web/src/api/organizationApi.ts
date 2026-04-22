import axios from '@/utils/request';
import {Response} from "@/utils/requestTypes.ts";

const prefix = '/organization';


export interface OrganizationTreeParams {
    level: number | null;
    parentId: string | null;
    searchValue?: string | null  // 新增搜索参数
}

export interface OrganizationTreeDetail {
    id: string | null;
    name: string;
    code: string | null;
    category: string | null;
    address: string | null;
    parentId: string | null;
    seq: number | null;
    enabled: boolean;
    children: OrganizationTreeDetail[];
    nameList: string[] | null;
    organizationIdList: string[] | null;
    hasChild: boolean | null;
    // 新增搜索相关字段
    isMatched?: boolean  // 是否匹配搜索条件
    hasMatchedChildren?: boolean  // 是否有匹配的子节点
}

export interface OrganizationTreeResponse extends Response {
    data: OrganizationTreeDetail[];
}

export const apiGetOrganizationTree = (params: OrganizationTreeParams): Promise<OrganizationTreeResponse> => {
    return axios.post(`${prefix}/tree`, params);
};


export interface OrganizationDetail {
    id: string | null;
    name: string;
    code: string | null;
    category: string | null;
    address: string | null;
    parentId: string | null;
    nameList: string[] | null;
    seq: number | null;
    enabled: boolean;
}

export const apiEditOrganization = (params: OrganizationDetail): Promise<Response> => {
    return axios.post(`${prefix}/edit`, params);
};

export interface OrganizationDetailResponse extends Response {
    data: OrganizationDetail;
}

export const apiGetOrganizationDetail = (menuId: string): Promise<OrganizationDetailResponse> => {
    return axios.get(`${prefix}/detail/${menuId}`);
};


export interface DeleteOrganizationParams {
    organizationId: string;
}

export const apiDeleteOrganization = (params: DeleteOrganizationParams): Promise<Response> => {
    return axios.post(`${prefix}/delete`, params);
};

export interface SaveOrganizationSeqAndParentParams {
    organizationTree: OrganizationTreeDetail[];
}

export const apiSaveOrganizationSeqAndParent = (params: SaveOrganizationSeqAndParentParams): Promise<Response> => {
    return axios.post(`${prefix}/save_seq_and_parent`, params);
};