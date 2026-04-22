import axios from '@/utils/request';
import { Response } from '@/utils/requestTypes.ts';

const prefix = '/quiz_play';

export interface UploadFileInfo {
    fileInfoId: string | null;
    fileName: string | null;
    fileType: string | null;
    fileSize: number | null;
    bucketName: string | null;
    objectName: string | null;
    fileObjectName: string | null;
    url: string | null;
    fileHash: string | null;
}

// ---- Entry ----
export interface HistoryItem {
    resultId: string;
    quizId: string;
    quizName: string;
    quizType: string;
    outcomeCode: string;
    outcomeName: string;
    outcomeSummary: string | null;
    outcomeAvatar: UploadFileInfo | null;
    score: number | null;
    createdAt: string | null;
}

export interface PublishedQuiz {
    quizId: string;
    quizName: string;
    quizType: string;
    covers: UploadFileInfo[] | null;
    shareTitle: string | null;
    shareDesc: string | null;
}

export interface QuizEntryData {
    status: 'active' | 'exhausted' | 'expired';
    maxUses: number | null;
    usedCount: number;
    hasHistory: boolean;
}

export interface QuizEntryResponse extends Response {
    data: QuizEntryData;
}

export interface QuizEntryParams {
    token: string;
}

export const apiGetQuizEntry = (params: QuizEntryParams): Promise<QuizEntryResponse> => {
    return axios.post(`${prefix}/entry`, { token: params.token });
};

export interface PageData<T> {
    pageIndex: number;
    pageSize: number;
    totalCount: number;
    filterCount: number;
    data: T[];
}

export interface QuizPageResponse extends Response {
    data: PageData<PublishedQuiz>;
}

export interface HistoryPageResponse extends Response {
    data: PageData<HistoryItem>;
}

export interface EntryPageParams {
    token: string;
    search?: string;
    pageIndex?: number;
    pageSize?: number;
}

export const apiGetEntryQuizzes = (params: EntryPageParams): Promise<QuizPageResponse> => {
    return axios.post(`${prefix}/entry/quizzes`, { token: params.token }, {
        params: {
            search: params.search ?? '',
            page_index: params.pageIndex ?? 1,
            page_size: params.pageSize ?? 20,
        },
    });
};

export const apiGetEntryHistory = (params: EntryPageParams): Promise<HistoryPageResponse> => {
    return axios.post(`${prefix}/entry/history`, { token: params.token }, {
        params: {
            search: params.search ?? '',
            page_index: params.pageIndex ?? 1,
            page_size: params.pageSize ?? 20,
        },
    });
};

// ---- Play ----
export interface QuizPlayOption {
    key: string;
    label: string;
    images: UploadFileInfo[] | null;
    nextQuestionSeq: number | null;
}

export interface QuizQuestion {
    seq: number;
    content: string;
    images: UploadFileInfo[] | null;
    isHidden: boolean;
    options: QuizPlayOption[];
    branchConfig: { defaultNextSeq?: number } | null;
}

export interface QuizPlayData {
    quizId: string;
    quizName: string;
    quizType: string;
    covers: UploadFileInfo[] | null;
    shareTitle: string | null;
    questions: QuizQuestion[];
    algoConfig: Record<string, any> | null;
    resultConfig: Record<string, any> | null;
}

export interface QuizPlayResponse extends Response {
    data: QuizPlayData;
}

export interface PlayDataParams {
    token: string;
    quizId: string;
}

export const apiGetPlayData = (params: PlayDataParams): Promise<QuizPlayResponse> => {
    return axios.post(`${prefix}/play`, { token: params.token }, { params: { quiz_id: params.quizId } });
};

// ---- Submit ----
export interface SubmitAnswersParams {
    token: string;
    quizId: string;
    answers: Record<string, string>;
}

export interface QuizResultData {
    resultId: string;
    quizId: string;
    quizName: string;
    quizType: string;
    outcomeCode: string;
    outcomeName: string;
    outcomeSummary: string | null;
    outcomeDetail: string | null;
    outcomeTags: string[] | null;
    outcomeAvatar: UploadFileInfo | null;
    score: number | null;
    calcResult: Record<string, any> | null;
    shareImage: UploadFileInfo | null;
    resultConfig: Record<string, any> | null;
}

export interface QuizResultResponse extends Response {
    data: QuizResultData;
}

export const apiSubmitAnswers = (params: SubmitAnswersParams): Promise<QuizResultResponse> => {
    return axios.post(
        `${prefix}/submit`,
        { token: params.token, answers: params.answers },
        { params: { quiz_id: params.quizId } },
    );
};

// ---- Result ----
export interface GetResultParams {
    token: string;
    resultId: string;
}

export const apiGetResult = (params: GetResultParams): Promise<QuizResultResponse> => {
    return axios.post(`${prefix}/result`, { token: params.token }, { params: { result_id: params.resultId } });
};
