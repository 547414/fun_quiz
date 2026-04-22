import axios from '@/utils/request';
import {Response} from "@/utils/requestTypes.ts";

const prefix = '/dept';


export interface DeptTreeParams {
    level: number | null;
    parentId: string | null;
    searchValue?: string | null  // 新增搜索参数
    organizationId?: string | null
}

export interface DeptTreeDetail {
    id: string | null;
    name: string;
    code: string | null;
    category: string | null;
    brief: string | null;
    parentId: string | null;
    sourceCategory: string | null;
    sourceId: string | null;
    seq: number | null;
    enabled: boolean;
    children: DeptTreeDetail[];
    nameList: string[] | null;
    deptIdList: string[] | null;
    hasChild: boolean | null;
    // 新增搜索相关字段
    isMatched?: boolean  // 是否匹配搜索条件
    hasMatchedChildren?: boolean  // 是否有匹配的子节点
}

export interface DeptTreeResponse extends Response {
    data: DeptTreeDetail[];
}

export const apiGetDeptTree = (params: DeptTreeParams): Promise<DeptTreeResponse> => {
    return axios.post(`${prefix}/tree`, params);
};


export interface DeptDetail {
    id: string | null;
    name: string;
    code: string | null;
    category: string | null;
    brief: string | null;
    parentId: string | null;
    sourceCategory: string | null;
    sourceId: string | null;
    nameList: string[] | null;
    seq: number | null;
    enabled: boolean;
}

export const apiEditDept = (params: DeptDetail): Promise<Response> => {
    return axios.post(`${prefix}/edit`, params);
};

export interface DeptDetailResponse extends Response {
    data: DeptDetail;
}

export const apiGetDeptDetail = (menuId: string): Promise<DeptDetailResponse> => {
    return axios.get(`${prefix}/detail/${menuId}`);
};


export interface DeleteDeptParams {
    deptId: string;
}

export const apiDeleteDept = (params: DeleteDeptParams): Promise<Response> => {
    return axios.post(`${prefix}/delete`, params);
};

export interface SaveDeptSeqAndParentParams {
    deptTree: DeptTreeDetail[];
}

export const apiSaveDeptSeqAndParent = (params: SaveDeptSeqAndParentParams): Promise<Response> => {
    return axios.post(`${prefix}/save_seq_and_parent`, params);
};