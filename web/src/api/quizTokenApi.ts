import axios from '@/utils/request';
import { Response } from '@/utils/requestTypes.ts';

const prefix = '/quiz_token';

export interface GenerateTokenParams {
    count: number;
    maxUses?: number | null;
    source?: string;
    batchCode?: string | null;
    expiresAt?: string | null;
    quizIds?: string[] | null;
    extra?: Record<string, any> | null;
}

export interface GeneratedTokensResult {
    tokens: string[];
    batchCode: string;
    count: number;
}

export interface GenerateTokenResponse extends Response {
    data: GeneratedTokensResult;
}

export const apiGenerateTokens = (params: GenerateTokenParams): Promise<GenerateTokenResponse> => {
    return axios.post(`${prefix}/generate`, params);
};

export interface TokenDetail {
    id: string;
    token: string;
    status: 'active' | 'exhausted' | 'expired';
    maxUses: number | null;
    usedCount: number;
    source: string;
    batchCode: string | null;
    expiresAt: string | null;
    quizIds: string[] | null;
    extra: Record<string, any> | null;
    createdAt: string;
}

export interface TokenPageParams {
    pageIndex: number;
    pageSize: number;
    batchCode?: string | null;
    status?: string | null;
}

export interface TokenPageResponse extends Response {
    data: {
        totalCount: number;
        pageIndex: number;
        pageSize: number;
        data: TokenDetail[];
    };
}

export const apiGetTokenPage = (params: TokenPageParams): Promise<TokenPageResponse> => {
    return axios.post(`${prefix}/page`, params);
};

export interface TokenDetailResponse extends Response {
    data: TokenDetail;
}

export interface GetTokenDetailParams {
    token: string;
}

export const apiGetTokenDetail = (params: GetTokenDetailParams): Promise<TokenDetailResponse> => {
    return axios.post(`${prefix}/detail/${params.token}`);
};

export interface UpdateTokenQuizIdsParams {
    tokenId: string;
    quizIds: string[] | null;
}

export const apiUpdateTokenQuizIds = (params: UpdateTokenQuizIdsParams): Promise<Response> => {
    return axios.post(`${prefix}/update_quiz_ids`, params);
};
