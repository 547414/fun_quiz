import axios from '@/utils/request';
import {Response} from "@/utils/requestTypes.ts";
import {WebUserLoginDetail} from "@/api/webUserApi.ts";

const prefix = '/union_user';


export const apiUnionUserLogout = (): Promise<Response> => {
    return axios.post(`${prefix}/logout`, {});
};

export interface DeleteUnionUserParams {
    unionUserId: string;
}

export const apiDeleteUnionUser = (params: DeleteUnionUserParams): Promise<Response> => {
    return axios.post(`${prefix}/delete`, params);
};

export interface UnionUserAuthCodeLoginParams {
    authCode: string;
}

export interface UnionUserAuthCodeLoginResponse extends Response {
    data: WebUserLoginDetail
}

export const apiUnionUserAuthCodeLogin = (params: UnionUserAuthCodeLoginParams): Promise<UnionUserAuthCodeLoginResponse> => {
    return axios.post(`${prefix}/auth_code_login`, params);
};