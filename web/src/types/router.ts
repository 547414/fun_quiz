// src/types/router.d.ts
import 'vue-router'

// 扩展 vue-router 的 RouteMeta 类型
declare module 'vue-router' {
    interface RouteMeta {
        needAuth: boolean;    // 是否需要认证
        alias: string;        // 别名
        key: string;       // 索引
        pathList: string[] | null, // 路径列表
        pathAliasList: string[] | null // 路径列表
    }
}
