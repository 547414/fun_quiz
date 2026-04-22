import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path';
import Components from 'unplugin-vue-components/vite';
import {VantResolver} from 'unplugin-vue-components/resolvers';
import AutoImport from 'unplugin-auto-import/vite';

export default defineConfig(({mode}) => {
    let outDir = 'dist/production';

    if (mode === 'development') {
        outDir = 'dist/development';
    } else if (mode === 'production') {
        outDir = 'dist/production';
    }

    return {
        plugins: [
            vue(),
            Components({
                resolvers: [VantResolver()],
            }),
            AutoImport({
                resolvers: [VantResolver()],
            }),
        ],
        resolve: {
            alias: {
                '@': path.resolve(__dirname, './src'),
            }
        },
        build: {
            outDir,
        },
        server: {
            allowedHosts: [
                'localhost',
                '127.0.0.1',
            ],
        },
        css: {
            preprocessorOptions: {
                scss: {
                    // 关键：避免 legacy-js-api 警告
                    api: 'modern-compiler', // 也可以用 'modern'
                },
            },
        },
    }
})
