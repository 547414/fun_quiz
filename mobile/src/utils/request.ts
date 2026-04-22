console.log('===== REQUEST.TS LOADED v4 =====');

import axios, {AxiosInstance, InternalAxiosRequestConfig, AxiosResponse, AxiosError, AxiosRequestConfig} from 'axios';
import {notifyError} from "@/utils/notify.ts";

class AuthError extends Error {
    constructor() {
        super('AUTH_REDIRECT');
        this.name = 'AuthError';
    }
}

const scene = "MOBILE";
const space = "MOBILE";

const getFormatUrl = (toUrl: string) => {
    if (toUrl === '/' || toUrl === '') {
        return 'None';
    }

    if (toUrl.startsWith('/')) {
        toUrl = toUrl.slice(1);
    }

    return toUrl
        .replace(/\//g, '_')
        .replace(/\?/g, '_*')
        .replace(/&/g, '*')
        .replace(/=/g, '_*_');
};

const baseService: AxiosInstance = axios.create({
    baseURL: import.meta.env.VITE_APP_BASE_API,
    timeout: 360000,
});

let isGoingToLogin = false;  // 新增标志位

const toGoLogin = () => {
    if (isGoingToLogin) return;  // 防止重复调用
    isGoingToLogin = true;

    notifyError('登录已过期，重新登录中...');
    localStorage.removeItem('unionUserInfo');
    sessionStorage.removeItem('unionUserInfo');
    setTimeout(() => {
        const baseUrl = import.meta.env.VITE_APP_BASE_URL
        const formatUrl = getFormatUrl(window.location.href);
        window.location.href = baseUrl + '/auth/wecom?action=TO_AUTH&redirect=' + formatUrl;
    }, 2000);
}

const whiteList: string[] = [
    '/auth/full_screen_auth_code_login',
    '/union_user/auth_code_login',
    '/union_user/refresh_access_token',
    '/debug',
    '/quiz_play',  // 测验移动端无需登录，token即身份
];

let isRefreshing = false;
let failedQueue: { resolve: (value: any) => void; reject: (reason?: any) => void; config: AxiosRequestConfig }[] = [];

const processQueue = (error: any, token: string | null = null) => {
    failedQueue.forEach((item) => {
        if (token) {
            const config = item.config;
            config.headers = {
                ...config.headers,
                'Authorization': `Bearer ${token}`,
            };
            baseService.request(config).then((res: any) => {
                item.resolve(res);
            }).catch((err: any) => {
                item.reject(err);
            });
        } else {
            item.reject(error);
        }
    });
    failedQueue = [];
};

const refreshToken = async (): Promise<string> => {
    let inLocalStorage = true;
    let userInfo = localStorage.getItem('unionUserInfo');
    if (!userInfo) {
        userInfo = sessionStorage.getItem('unionUserInfo');
        inLocalStorage = false;
    }

    if (!userInfo) {
        return Promise.reject(new Error('No user info'));
    }

    const parsedUserInfo = JSON.parse(userInfo);
    const refreshTokenStr = parsedUserInfo?.refreshToken;
    const unionUserId = parsedUserInfo?.unionUserInfo?.id;

    if (!refreshTokenStr) {
        return Promise.reject(new Error('No refresh token'));
    }

    const response = await axios.post(
        `${import.meta.env.VITE_APP_BASE_API}/union_user/refresh_access_token`,
        {refreshToken: refreshTokenStr, unionUserId: unionUserId},
        {
            headers: {
                'Scene': `${scene}`,
                'Space': `${space}`
            }
        }
    );
    if (response.status === 200 && response.data.code === 200) {
        const newToken = response.data.data.accessToken;
        parsedUserInfo.accessToken = newToken;

        if (inLocalStorage) {
            localStorage.setItem('unionUserInfo', JSON.stringify(parsedUserInfo));
        } else {
            sessionStorage.setItem('unionUserInfo', JSON.stringify(parsedUserInfo));
        }

        return newToken;
    } else {
        return Promise.reject(new Error('Refresh failed'));
    }
};

// 请求拦截器 - 只负责添加 headers
baseService.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
        const isWhiteListed = whiteList.some((path) => config.url?.includes(path));
        if (!isWhiteListed) {
            let userInfo = localStorage.getItem('unionUserInfo');
            if (!userInfo) {
                userInfo = sessionStorage.getItem('unionUserInfo');
            }
            if (userInfo) {
                const parsedUserInfo = JSON.parse(userInfo);
                const token = parsedUserInfo?.accessToken;
                if (token) {
                    config.headers['Authorization'] = `Bearer ${token}`;
                    config.headers['Scene'] = `${scene}`;
                    config.headers['Space'] = `${space}`;
                } else {
                    toGoLogin()
                }
            } else {
                if (!config.url?.includes('/login') && !config.url?.includes('/web_oauth_login')) {
                    toGoLogin()
                }
            }
        } else {
            config.headers['Scene'] = `${scene}`;
            config.headers['Space'] = `${space}`;
        }

        return config;
    },
    (error: AxiosError) => {
        console.error(error);
        return Promise.reject(error);
    }
);

// 响应拦截器 - 只负责返回 response.data，不处理 401
baseService.interceptors.response.use(
    (response: AxiosResponse) => {
        return response.data;
    },
    (error: AxiosError) => {
        if (error.response?.status === 403) {
            const responseData: any = error.response.data;
            return Promise.reject(responseData?.detail?.message);
        }
        return Promise.reject(error);
    }
);

// 包装函数：处理 401 和 token 刷新
const request = <T = any>(config: AxiosRequestConfig): Promise<T> => {
    return new Promise((resolve, reject) => {
        baseService.request<any, T>(config).then((res) => {
            resolve(res);
        }).catch((error: AxiosError) => {
            if (error.response?.status !== 401) {
                reject(error);
                return;
            }

            // 处理 401
            const originalConfig = error.config as AxiosRequestConfig & { _retry?: boolean };

            if (originalConfig._retry) {
                toGoLogin();
                reject(error);
                return;
            }

            if (isRefreshing) {
                failedQueue.push({resolve, reject, config: originalConfig});
                return;
            }

            originalConfig._retry = true;
            isRefreshing = true;

            refreshToken().then((newToken) => {
                processQueue(null, newToken);
                isRefreshing = false;

                // 重试原始请求
                originalConfig.headers = {
                    ...originalConfig.headers,
                    'Authorization': `Bearer ${newToken}`,
                };

                baseService.request<any, T>(originalConfig).then((res) => {
                    resolve(res);
                }).catch((err) => {
                    reject(err);
                });
            }).catch((err) => {
                processQueue(err, null);
                isRefreshing = false;
                toGoLogin();
                reject(new AuthError());  // 抛出特殊错误
            });
        });
    });
};

// 导出一个兼容 axios 接口的对象
const service = {
    request: <T = any>(config: AxiosRequestConfig): Promise<T> => request<T>(config),
    get: <T = any>(url: string, config?: AxiosRequestConfig): Promise<T> => request<T>({...config, method: 'get', url}),
    post: <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => request<T>({
        ...config,
        method: 'post',
        url,
        data
    }),
    put: <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => request<T>({
        ...config,
        method: 'put',
        url,
        data
    }),
    delete: <T = any>(url: string, config?: AxiosRequestConfig): Promise<T> => request<T>({
        ...config,
        method: 'delete',
        url
    }),
    patch: <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => request<T>({
        ...config,
        method: 'patch',
        url,
        data
    }),
};

export default service;