import axios from '@/utils/request';
import { Response } from '@/utils/requestTypes.ts';
import { UploadFileInfo } from '@/api/storageApi.ts';

const prefix = '/quiz';

export type QuizType = 'vector' | 'score' | 'branch' | 'random';
export type QuizStatus = 'draft' | 'published' | 'archived';

export interface ImagePrompt {
    prompt: string;
    style?: string | null;
    negativePrompt?: string | null;
}

export interface QuizDetail {
    id: string;
    name: string;
    code: string;
    covers: UploadFileInfo[] | null;
    coverPrompt?: ImagePrompt | null;
    quizType: QuizType;
    status: QuizStatus;
    source: string;
    sortOrder: number;
    shareTitle: string | null;
    shareDesc: string | null;
    fallbackOutcomeCode: string | null;
    algoConfig: Record<string, any> | null;
    specialRules: Record<string, any>[] | null;
    resultConfig: Record<string, any> | null;
    questionCount?: number;
    outcomeCount?: number;
    participateCount?: number;
    createdAt: string;
    updatedAt: string;
}

export interface QuizPageParams {
    pageIndex: number;
    pageSize: number;
    search?: string | null;
    quizType?: QuizType | null;
    status?: QuizStatus | null;
}

export interface PageData<T> {
    pageIndex: number;
    pageSize: number;
    totalCount: number;
    filterCount: number;
    data: T[];
}

export interface QuizPageResponse extends Response {
    data: PageData<QuizDetail>;
}

export interface QuizDetailResponse extends Response {
    data: QuizDetail;
}

export const apiGetQuizPage = (params: QuizPageParams): Promise<QuizPageResponse> => {
    return axios.post(`${prefix}/page`, params);
};

export interface QuizDetailParams {
    quizId: string;
}

export const apiGetQuizDetail = (params: QuizDetailParams): Promise<QuizDetailResponse> => {
    return axios.post(`${prefix}/detail/${params.quizId}`);
};

export const apiEditQuiz = (params: Partial<QuizDetail>): Promise<Response> => {
    return axios.post(`${prefix}/edit`, params);
};

export interface DeleteQuizParams {
    quizId: string;
}

export const apiDeleteQuiz = (params: DeleteQuizParams): Promise<Response> => {
    return axios.post(`${prefix}/delete`, params);
};

export interface ChangeQuizStatusParams {
    quizId: string;
    status: QuizStatus;
}

export const apiChangeQuizStatus = (params: ChangeQuizStatusParams): Promise<Response> => {
    return axios.post(`${prefix}/change_status`, params);
};

export interface ImportQuizParams {
    definition: Record<string, any>;
}

export interface ImportQuizResponse extends Response {
    data: { quizId: string };
}

export const apiImportQuiz = (params: ImportQuizParams): Promise<ImportQuizResponse> => {
    return axios.post(`${prefix}/import`, params);
};

// 题目
export interface QuizOption {
    key: string;
    label: string;
    images?: UploadFileInfo[] | null;
    imagePrompt?: ImagePrompt | null;
    dimScores?: Record<string, number> | null;
    score?: number | null;
    nextQuestionSeq?: number | null;
    outcomeCode?: string | null;
}

export interface QuizQuestion {
    id?: string;
    quizId?: string;
    seq: number;
    content: string;
    images?: UploadFileInfo[] | null;
    imagePrompt?: ImagePrompt | null;
    isHidden: boolean;
    options: QuizOption[];
    branchConfig?: Record<string, any> | null;
}

export interface QuestionsResponse extends Response {
    data: QuizQuestion[];
}

export interface GetQuestionsParams {
    quizId: string;
}

export const apiGetQuestions = (params: GetQuestionsParams): Promise<QuestionsResponse> => {
    return axios.post(`${prefix}/questions/${params.quizId}`);
};

export interface BatchSaveQuestionsParams {
    quizId: string;
    questions: QuizQuestion[];
}

export const apiBatchSaveQuestions = (params: BatchSaveQuestionsParams): Promise<Response> => {
    return axios.post(`${prefix}/questions/batch_save`, params);
};

// 结果
export interface QuizOutcome {
    id?: string;
    quizId?: string;
    code: string;
    name: string;
    avatar?: UploadFileInfo | null;
    avatarPrompt?: ImagePrompt | null;
    summary?: string | null;
    detail?: string | null;
    tags?: string[] | null;
    sortOrder: number;
    isFallback: boolean;
    isSpecial: boolean;
    matchConfig?: Record<string, any> | null;
}

export interface OutcomesResponse extends Response {
    data: QuizOutcome[];
}

export interface GetOutcomesParams {
    quizId: string;
}

export const apiGetOutcomes = (params: GetOutcomesParams): Promise<OutcomesResponse> => {
    return axios.post(`${prefix}/outcomes/${params.quizId}`);
};

export interface BatchSaveOutcomesParams {
    quizId: string;
    outcomes: QuizOutcome[];
}

export const apiBatchSaveOutcomes = (params: BatchSaveOutcomesParams): Promise<Response> => {
    return axios.post(`${prefix}/outcomes/batch_save`, params);
};

// 统计
export interface OutcomeDistributionItem {
    outcomeCode: string;
    outcomeName: string;
    count: number;
}

export interface QuizStats {
    quizId: string;
    quizName: string;
    totalTokens: number;
    usedTokens: number;
    outcomeDistribution: OutcomeDistributionItem[];
}

export interface QuizStatsResponse extends Response {
    data: QuizStats;
}

export interface GetQuizStatsParams {
    quizId: string;
}

export const apiGetQuizStats = (params: GetQuizStatsParams): Promise<QuizStatsResponse> => {
    return axios.post(`${prefix}/stats/${params.quizId}`);
};
