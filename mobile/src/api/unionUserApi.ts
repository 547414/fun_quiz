import axios from '@/utils/request';
import {Response} from "@/utils/requestTypes.ts";

const prefix = '/union_user';


export interface EditUnionUserInfoParams {
    unionUserId: string;
    name: string;
    company: string;
    dept: string;
    position: string;
}


export const apiEditUnionUserInfo = (params: EditUnionUserInfoParams): Promise<Response> => {
    return axios.post(`${prefix}/edit_info`, params);
};

export interface UnionUserAuthCodeLoginParams {
    authCode: string;
}

export interface UnionUserAuthCodeLoginResponse extends Response {
    data: UnionUserAuthCodeLogin;
}

export interface UnionUserAuthCodeLogin {
    accessToken: string;
    refreshToken: string;
    tokenType: string;
    unionUserInfo: unionUserInfo;
    scene?: string | null;
    space?: string | null;
}

export interface unionUserInfo {
    id: string;
    name: string | null;
    companyId: string | null;
    company: string | null;
    dept: string | null;
    position: string | null;
    userList: UnionUserInfoListDetailModel[];
}

export interface UnionUserInfoListDetailModel {
    unionUserUserCategory: string;
    unionUserUserId: string;
}

export const apiUnionUserAuthCodeLogin = (params: UnionUserAuthCodeLoginParams): Promise<UnionUserAuthCodeLoginResponse> => {
    return axios.post(`${prefix}/auth_code_login`, params);
};
