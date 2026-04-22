import axios from '@/utils/request';
import {Response} from "@/utils/requestTypes.ts";

const prefix = '/menu';


export interface MenuTreeParams {
    parentId: string | null;
}

export interface MenuTreeDetail {
    id?: string;
    parentId?: string | null;
    seq?: number;
    name: string;
    code?: string;
    enabled: boolean;
    url?: string;
    icon?: string;
    label?: string | null;
    path?: string | null;
    type?: string;
    typeDisplay?: string;
    children?: MenuTreeDetail[];
    nameList?: string[] | null;
}

export interface MenuTreeResponse extends Response {
    data: MenuTreeDetail[];
}

export const apiGetMenuTree = (params: MenuTreeParams): Promise<MenuTreeResponse> => {
    return axios.post(`${prefix}/tree`, params);
};

export const apiGetAllowMenuTree = (params: MenuTreeParams): Promise<MenuTreeResponse> => {
    return axios.post(`${prefix}/allow_menu_tree`, params);
};


export interface MenuPageParams {
    pageSize: number;
    pageIndex: number;
    search: string | null;
    searchFields: string[] | null;
}

export interface MenuPageResponse extends Response {
    data: {
        filterCount: number;
        pageIndex: number;
        pageSize: number;
        totalCount: number;
        data: MenuTreeDetail[];
    }
}

export const apiGetMenuPage = (params: MenuPageParams): Promise<MenuPageResponse> => {
    return axios.post(`${prefix}/page`, params);
};

export interface MenuDetail {
    id: string | null;
    name: string;
    code: string;
    enabled: boolean;
    url: string;
    icon: string;
    type: string;
    parentId: string | null;
    seq: number | null;
    nameList: string[] | null;
}

export const apiEditMenu = (params: MenuDetail): Promise<Response> => {
    return axios.post(`${prefix}/edit`, params);
};

export interface MenuDetailResponse extends Response {
    data: MenuDetail;
}

export const apiGetMenuDetail = (menuId: string): Promise<MenuDetailResponse> => {
    return axios.get(`${prefix}/detail/${menuId}`);
};


export interface DeleteMenuParams {
    menuId: string;
}

export const apiDeleteMenu = (params: DeleteMenuParams): Promise<Response> => {
    return axios.post(`${prefix}/delete`, params);
};

export interface SaveMenuSeqAndParentParams {
    menuTree: MenuTreeDetail[];
}

export const apiSaveMenuSeqAndParent = (params: SaveMenuSeqAndParentParams): Promise<Response> => {
    return axios.post(`${prefix}/save_seq_and_parent`, params);
};
