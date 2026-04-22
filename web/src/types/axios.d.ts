// src/types/axios.d.ts
import 'axios';

declare module 'axios' {
    export interface AxiosRequestConfig<D = any> {
        returnFullResponse?: boolean; // 自定义属性
    }
}
