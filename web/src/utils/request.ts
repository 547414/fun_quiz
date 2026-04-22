import axios, {AxiosInstance, InternalAxiosRequestConfig, AxiosResponse, AxiosError} from 'axios';

const service: AxiosInstance = axios.create({
    baseURL: import.meta.env.VITE_APP_BASE_API,
    timeout: 360000,
});

const scene = "WEB";
const space = "WEB";

const toGoLogin = (debugInfo: string = null) => {
    if (debugInfo) {
        console.log(`to login ... ${debugInfo}`)
        // ElNotification({
        //     title: '登录已过期，请重新登录',
        //     message: debugInfo,
        //     type: 'error',
        // })
    } else {
        // ElNotification({
        //     title: '登录已过期，请重新登录',
        //     type: 'error',
        // })
    }
    localStorage.removeItem('unionUserInfo');
    sessionStorage.removeItem('unionUserInfo');
    setTimeout(() => {
        window.location.href = '/login';
    }, 2000);
}
// 白名单列表，不需要添加 Authorization 的接口
const whiteList: string[] = [
    '/auth/login',
    '/auth/register',
    '/union_user/auth_code_login',
    '/union_user/refresh_token',
    '/auth/web_oauth_login',
    '/wx_public_account/qr_code_url',
    '/auth/qr_code',
    '/captcha/generate',
    '/captcha/validate',
    '/company/page',
    '/user/register',
];

// 用于标识是否正在刷新 token
let isRefreshing = false;
// 存储等待刷新的请求队列
let failedQueue: any[] = [];

const processQueue = (error: any, token: string | null = null) => {
    failedQueue.forEach((prom) => {
        if (token) {
            prom.resolve(token);
        } else {
            prom.reject(error);
        }
    });
    failedQueue = [];
};

// 请求拦截器
service.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
        // 判断当前请求是否在白名单列表中
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
                    // 判断是否 restPassword, 是则跳到重置密码的页面
                    if (parsedUserInfo?.user?.resetPassword && !config.url.includes('/reset_self_password')) {
                        window.location.href = '/reset-password';
                    }
                    config.headers['Authorization'] = `Bearer ${token}`;
                    config.headers['Space'] = `${space}`;
                    config.headers['Scene'] = `${scene}`;
                } else {
                    toGoLogin('1')
                }
            } else {
                if (!config.url?.includes('/login') && !config.url?.includes('/web_oauth_login')) {
                    toGoLogin(config.url)
                } else {
                    config.headers['Space'] = `${space}`;
                    config.headers['Scene'] = `${scene}`;
                }
            }
        } else {
            console.log('refresh token white list ...')
            config.headers['Space'] = `${space}`;
            config.headers['Scene'] = `${scene}`;
        }

        return config;
    },
    (error: AxiosError) => {
        console.error(error);
        return Promise.reject(error);
    }
);

// 响应拦截器
service.interceptors.response.use(
    (response: AxiosResponse) => {
        // 检查配置项中是否设置了 returnFullResponse
        if (response.config?.returnFullResponse) {
            return response; // 返回完整的响应对象
        }
        return response.data;
    },
    async (error: AxiosError) => {
        const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };
        // 如果响应状态为401并且请求没有被重试过
        if (error.response?.status === 401 && !originalRequest._retry) {
            if (isRefreshing) {
                return new Promise(function (resolve, reject) {
                    failedQueue.push({resolve, reject});
                }).then((token) => {
                    originalRequest.headers['Authorization'] = `Bearer ${token}`;
                    originalRequest.headers['Space'] = `${space}`;
                    originalRequest.headers['Scene'] = `${scene}`;
                    return axios(originalRequest);
                }).catch((err) => {
                    return Promise.reject(err);
                });
            }
            originalRequest._retry = true;
            isRefreshing = true;
            let inLocalStorage = true
            let userInfo = localStorage.getItem('unionUserInfo');
            if (!userInfo) {
                userInfo = sessionStorage.getItem('unionUserInfo');
                inLocalStorage = false
            }
            let toLogin = false;
            if (userInfo) {
                const parsedUserInfo = JSON.parse(userInfo);
                const refreshToken = parsedUserInfo?.refreshToken;
                if (refreshToken) {
                    try {
                        const response = await axios.post(
                            `${import.meta.env.VITE_APP_BASE_API}/union_user/refresh_access_token`,
                            {refresh_token: refreshToken},
                            {
                            headers: {
                                'Space': `${space}`,
                                'Scene': `${scene}`
                            }
                        }
                        );
                        if (response.status === 200) {
                            if (response.data.code === 200) {
                                parsedUserInfo.accessToken = response.data.data.accessToken;
                                if (inLocalStorage) {
                                    localStorage.setItem('unionUserInfo', JSON.stringify(parsedUserInfo));
                                } else {
                                    sessionStorage.setItem('unionUserInfo', JSON.stringify(parsedUserInfo));
                                }
                                console.log('response ...')
                                console.log(response)
                                originalRequest.headers['Authorization'] = `Bearer ${response.data.data.accessToken}`;
                                originalRequest.headers['Space'] = `${space}`;
                                originalRequest.headers['Scene'] = `${scene}`;
                                processQueue(null, response.data.data.accessToken);
                                // 重新发起请求
                                const retryResponse = await axios(originalRequest);
                                if (retryResponse.status === 401) {
                                    toLogin = true;
                                } else {
                                    isRefreshing = false;
                                    return retryResponse.data;
                                }
                            } else {
                                toLogin = true;
                            }
                            toLogin = true;
                        }
                        if (toLogin) {
                            toGoLogin('3');
                        }
                    } catch (err) {
                        processQueue(err, null);
                        return Promise.reject(err);
                    } finally {
                        isRefreshing = false;
                    }
                } else {

                }
            } else {
                toLogin = true;
            }
            if (toLogin) {
                toGoLogin('4');
            }
        }
        if (error.response?.status === 403) {
            const responseData: any = error.response.data;
            return Promise.reject(responseData?.detail?.message);
        } else {
            return Promise.reject(error);
        }
    }
);


export default service;
