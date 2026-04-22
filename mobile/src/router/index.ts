// src/router/index.ts
import {createRouter, createWebHistory} from 'vue-router'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: () => import('@/views/Home.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/quiz',
            name: 'QuizEntry',
            component: () => import('@/views/quiz/Entry.vue'),
            meta: { requiresAuth: false }
        },
        {
            path: '/quiz/intro',
            name: 'QuizIntro',
            component: () => import('@/views/quiz/Intro.vue'),
            meta: { requiresAuth: false }
        },
        {
            path: '/quiz/play',
            name: 'QuizPlay',
            component: () => import('@/views/quiz/Play.vue'),
            meta: { requiresAuth: false }
        },
        {
            path: '/quiz/result',
            name: 'QuizResult',
            component: () => import('@/views/quiz/Result.vue'),
            meta: { requiresAuth: false }
        },
        {
            path: '/quiz/error',
            name: 'QuizError',
            component: () => import('@/views/sys/Error.vue'),
            meta: { requiresAuth: false }
        },
        {
            path: '/debug',
            name: 'Debug',
            component: () => import('@/views/sys/Debug.vue'),
            meta: {
                requiresAuth: false,
            }
        }
    ],
})

// 全局路由守卫
router.beforeEach((_to, _from, next) => {
    // if (to.meta.requiresAuth) {
    //     // 验证逻辑，当前是根据url中的 ?token= 做验证的，此系统没必要设计的很复杂，如此足矣
    // }
    next();
});

export default router
