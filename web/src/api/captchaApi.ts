import axios from '@/utils/request';
import {Response} from "@/utils/requestTypes.ts";

const prefix = '/captcha';


export interface CaptchaDetail extends Response {
    captchaId: string;
    correctTexts: string[];
    correctPinyinTexts: string[];
    captchaBase64: string;
}

export interface GenerateCaptchaResponse extends Response {
    data: CaptchaDetail;
}

export const apiGenerateCaptcha = (): Promise<GenerateCaptchaResponse> => {
    return axios.post(`${prefix}/generate`, {});
};

export interface ValidateCaptchaTextPositionsParams {
    text: string;
    x: number;
    y: number;
}

export interface ValidateCaptchaParams {
    captchaId: string;
    textPositions: ValidateCaptchaTextPositionsParams[];
}

export interface ValidateCaptchaResponse extends Response {
    data: string;
}

export const apiValidateCaptcha = (params: ValidateCaptchaParams): Promise<ValidateCaptchaResponse> => {
    return axios.post(`${prefix}/validate`, params);
};

