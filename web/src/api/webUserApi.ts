import axios from '@/utils/request';
import {Response} from "@/utils/requestTypes.ts";
import {PageSortEnum} from "@/enum/pageSortEnum.ts";
import {FileDetail} from "@/api/storageApi.ts";

const prefix = '/web_user';


export interface WebUserLoginParams {
    name: string | null;
    password: string | null;
    verificationCode: string | null;
    sceneId: string | null;
    unionUserId: string | null;
    captchaId: string | null;
    validateCaptchaAuthCode: string | null;
    agreement: boolean | null;
    remember: boolean | null;
}

export interface WebUserLoginResponse extends Response {
    data: WebUserLoginDetail
}

export interface WebUserInfoRole {
    roleCode: string;
    roleName: string;
}

export interface UserRoleListInfo {
    roleCode: string;
    roleName: string;
}

export interface UserListItemOrganization {
    id: string;
    name: string;
    nameList: string[];
}

export interface UserListItemDept {
    id: string;
    name: string;
    nameList: string[];
}

export interface UserListInfo {
    unionUserUserCategory: string | null;
    unionUserUserId: string | null;
    unionUserUserName: string | null;
    unionUserUserRoleList: UserRoleListInfo[] | null;
    currentRoleCode: string | null;
    organizationList: UserListItemOrganization[] | null;
    deptList: UserListItemDept[] | null;
}

export interface UnionUserInfo {
    id: string;
    name: string | null;
    userList: UserListInfo[] | null;
}

export interface WebUserLoginDetail {
    accessToken: string;
    refreshToken: string;
    tokenType: string;
    unionUserInfo: UnionUserInfo;
    scene?: string | null;
    space?: string | null;
}

export const apiWebUserLogin = (params: WebUserLoginParams): Promise<WebUserLoginResponse> => {
    return axios.post(`${prefix}/login`, params);
};

export interface WebOauthLoginParams {
    authCode: string;
    wecomUserUuid: string;
}

export const apiWebOauthLogin = (params: WebOauthLoginParams): Promise<WebUserLoginResponse> => {
    return axios.post(`${prefix}/web_oauth_login`, params);
};


export interface AddWebUserParams {
    name: string;
    roleCodeList: string[];
    password: string;
    passwordRepeat: string;
    mobile: string | null;
    email: string | null;
    avatarFileInfo: FileDetail | null;
    wecomUserUuid: string | null;
    unionUserUuid: string | null;
    wxUserId: string | null;
    enabled: boolean;
    companyId: string | null;
    company: string | null;
    dept: string | null;
    position: string | null;
}

export const apiAddWebUser = (params: AddWebUserParams): Promise<Response> => {
    return axios.post(`${prefix}/add`, params);
};


export interface EditWebUserParams {
    id: string;
    name: string;
    roleCodeList: string[];
    password: string;
    passwordRepeat: string;
    mobile: string | null;
    email: string | null;
    avatarFileInfo: FileDetail | null;
    wecomUserUuid: string;
    enabled: boolean;
    organizationList: UserListItemOrganization[] | null;
    deptList: UserListItemDept[] | null;
}

export const apiEditWebUser = (params: EditWebUserParams): Promise<Response> => {
    return axios.post(`${prefix}/edit`, params);
};


export interface WebUserPageParams {
    pageSize: number;
    pageIndex: number;
    search: string | null;
    nameSort: PageSortEnum | null;
    roleCodeList: string[] | null;
    searchFields: string[] | null;
}

export interface WebUserPageResponse extends Response {
    data: {
        filterCount: number;
        pageIndex: number;
        pageSize: number;
        totalCount: number;
        data: WebUserDetail[];
    }
}

export interface WebUserDetail {
    id: string;
    name: string;
    unionUserUuid: string | null;
    mobile: string | null;
    email: string | null;
    enabled: boolean;
    avatarFileInfo: FileDetail | null;
    roleList: WebUserInfoRole[];
    organizationList: UserListItemOrganization[] | null;
    deptList: UserListItemDept[] | null;
}

export const apiGetWebUserPage = (params: WebUserPageParams): Promise<WebUserPageResponse> => {
    return axios.post(`${prefix}/page`, params);
};

export interface WebUserListParams {
    userIdList: string[];
}

export interface WebUserListResponse extends Response {
    data: WebUserDetail[];
}

export const apiGetWebUserByIdList = (params: WebUserListParams): Promise<WebUserListResponse> => {
    return axios.post(`${prefix}/get_by_id_list`, params);
};


export interface ChangeWebUserEnabledParams {
    id: string;
    enabled: boolean;
}

export const apiChangeWebUserEnabled = (params: ChangeWebUserEnabledParams): Promise<Response> => {
    return axios.post(`${prefix}/change_enabled`, params);
};


export interface WebUserDetailResponse extends Response {
    data: WebUserDetail
}

export const apiGetWebUserDetail = (userId: string): Promise<WebUserDetailResponse> => {
    return axios.get(`${prefix}/detail/${userId}`);
};


export interface ResetSelfPasswordParams {
    oldPassword: string;
    newPassword: string;
    newPasswordRepeat: string;
}

export const apiResetSelfPassword = (params: ResetSelfPasswordParams): Promise<Response> => {
    return axios.post(`${prefix}/reset_self_password`, params);
};


export interface ResetPasswordParams {
    userId: string;
}

export const apiResetPassword = (params: ResetPasswordParams): Promise<Response> => {
    return axios.post(`${prefix}/reset_password`, params);
};

export interface ChangeCurrentUserRoleParams {
    roleCode: string;
}

export const apiChangeCurrentUserRole = (params: ChangeCurrentUserRoleParams): Promise<WebUserLoginResponse> => {
    return axios.post(`${prefix}/change_current_user_role`, params);
};

export interface UserRegisterParams {
    captchaId: string;
    validateAuthCode: string;
    name: string;
    password: string;
    companyId: string;
    company: string;
    dept: string | null;
    position: string | null;
    inviteCode: string | null;
}

export const apiUserRegister = (params: UserRegisterParams): Promise<Response> => {
    return axios.post(`${prefix}/register`, params);
};
