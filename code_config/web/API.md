# web api 约定

参考：`web/src/api/menuApi.ts`

## 规则

- 文件名 `xxxApi.ts`，放在 `src/api/`
- `const prefix = '/xxx'`，与后端 router 模块名对应
- 接口（interface）用 camelCase，字段与后端 model `model_dump()` 输出的 camelCase 一致
- 响应类型继承 `Response`（从 `@/utils/requestTypes.ts` 导入）
- 导出 `apiXxxAction` 格式的函数，返回 `Promise<XxxResponse>`
- 函数参数必须用 interface 封装，不允许裸参数；调用时先声明带类型的 params 变量再传入函数
- 文件下载用 `responseType: 'blob'`

## 示例骨架

```typescript
import axios from '@/utils/request';
import { Response } from '@/utils/requestTypes.ts';

const prefix = '/xxx';

export interface XxxDetail {
    id: string;
    name: string;
}

export interface XxxPageParams {
    pageIndex: number;
    pageSize: number;
    search: string | null;
}

export interface XxxPageResponse extends Response {
    data: { totalCount: number; data: XxxDetail[] };
}

export interface XxxDetailParams {
    id: string;
}

export const apiGetXxxPage = (params: XxxPageParams): Promise<XxxPageResponse> => {
    return axios.post(`${prefix}/page`, params);
};

export const apiGetXxxDetail = (params: XxxDetailParams): Promise<Response> => {
    return axios.get(`${prefix}/detail/${params.id}`);
};
```

## 调用示例

```typescript
// 先声明带类型的 params 变量，再传入函数
const xxxDetailParams: XxxDetailParams = {
    id: id,
}
apiGetXxxDetail(xxxDetailParams).then(res => {
    if (res.code === 200) {
        detail.value = res.data
    }
}).finally(() => {
    loading.value = false
})
```
