type ApiResult<T> = {
  code: number;
  message: string;
  data: T;
};

type RequestOptions = {
  retryOnUnauthorized?: boolean;
  autoRedirectOnAuthFail?: boolean;
  scene?: string;
  space?: string;
};

export class ApiClientError extends Error {
  code: number;
  status: number;

  constructor(message: string, code: number, status: number) {
    super(message);
    this.name = "ApiClientError";
    this.code = code;
    this.status = status;
  }
}

function mapErrorMessage(code: number, fallbackMessage: string) {
  const codeMap: Record<number, string> = {
    400: "请求参数错误",
    401: "登录已失效，请重新登录",
    403: "没有权限执行该操作",
    404: "请求资源不存在",
    409: "数据冲突，请刷新后重试",
    429: "请求过于频繁，请稍后再试",
    500: "服务器异常，请稍后再试",
    50001: "安全验证失效，请重新操作",
  };
  return codeMap[code] ?? fallbackMessage ?? "请求失败";
}

function shouldRedirectToLogin(options?: RequestOptions) {
  if (typeof window === "undefined") return false;
  if (options?.autoRedirectOnAuthFail === false) return false;
  if (window.location.pathname === "/login") return false;
  return true;
}

function resolveSceneSpace(options?: RequestOptions) {
  if (options?.scene || options?.space) {
    return {
      scene: options.scene ?? "WEB",
      space: options.space ?? "WEB",
    };
  }
  if (typeof window !== "undefined") {
    const path = window.location.pathname;
    const h5ExactPaths = new Set(["/quiz"]);
    const h5PrefixPaths = ["/quiz/intro", "/quiz/play", "/quiz/result", "/quiz/error"];
    if (h5ExactPaths.has(path) || h5PrefixPaths.some((item) => path === item || path.startsWith(`${item}/`))) {
      return {
        scene: "H5",
        space: "H5",
      };
    }
  }
  if (typeof window !== "undefined") {
    return {
      scene: "WEB",
      space: "WEB",
    };
  }
  return {
    scene: "WEB",
    space: "WEB",
  };
}

function redirectToLogin() {
  if (typeof window === "undefined") return;
  const currentPath = `${window.location.pathname}${window.location.search}`;
  const encoded = encodeURIComponent(currentPath);
  window.location.href = `/login?redirect=${encoded}`;
}

function buildHeaders(options?: RequestOptions) {
  const { scene, space } = resolveSceneSpace(options);
  return {
    "Content-Type": "application/json",
    Scene: scene,
    Space: space,
  };
}

async function tryRefreshToken(options?: RequestOptions) {
  const response = await fetch("/api/union_user/refresh_access_token", {
    method: "POST",
    headers: buildHeaders(options),
    credentials: "include",
    body: JSON.stringify({}),
  });
  const json = (await response.json()) as ApiResult<unknown>;
  return json.code === 200;
}

async function requestJson<T>(method: "GET" | "POST", url: string, body?: unknown, options?: RequestOptions): Promise<T> {
  const response = await fetch(url, {
    method,
    headers: buildHeaders(options),
    credentials: "include",
    body: method === "GET" ? undefined : JSON.stringify(body ?? {}),
  });

  const json = (await response.json().catch(() => null)) as ApiResult<T> | null;
  if (!json) {
    throw new ApiClientError("服务响应格式异常", response.status || 500, response.status || 500);
  }

  if (json.code === 401 && options?.retryOnUnauthorized !== false && url !== "/api/union_user/refresh_access_token") {
    const refreshed = await tryRefreshToken(options);
    if (refreshed) {
      return requestJson<T>(method, url, body, {
        ...options,
        retryOnUnauthorized: false,
      });
    }
    if (shouldRedirectToLogin(options)) {
      redirectToLogin();
    }
  }

  if (json.code !== 200) {
    const message = mapErrorMessage(json.code, json.message);
    if (json.code === 401 && shouldRedirectToLogin(options)) {
      redirectToLogin();
    }
    throw new ApiClientError(message, json.code, response.status || 500);
  }

  return json.data;
}

export async function postJson<T>(url: string, body?: unknown, options?: RequestOptions): Promise<T> {
  return requestJson<T>("POST", url, body, options);
}

export async function getJson<T>(url: string, options?: RequestOptions): Promise<T> {
  return requestJson<T>("GET", url, undefined, options);
}

export const apiClient = {
  post: postJson,
  get: getJson,
};
