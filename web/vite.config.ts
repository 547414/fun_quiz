import {defineConfig, UserConfig} from 'vite'
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
        css: {
            preprocessorOptions: {
                scss: {
                    api: 'modern-compiler' // or "modern"
                }
            }
        },
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
            host: '0.0.0.0',
            // 明确允许的 Host 列表
            allowedHosts: [
                'localhost',
                '127.0.0.1',
            ],
        }
    } as UserConfig
})
