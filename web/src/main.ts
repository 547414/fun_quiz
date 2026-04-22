import {createApp} from 'vue'
import App from './App.vue'
import router from './router'
import {Icon} from '@iconify/vue';
import {createPinia} from 'pinia';
import './public.scss'
import './style.css'
import Viewer from 'v-viewer';
import 'viewerjs/dist/viewer.css';
import naive from 'naive-ui'

const app = createApp(App)

const pinia = createPinia();

app.use(router)
app.use(naive)
app.use(pinia);

app.use(Viewer, {
    defaultOptions: {
        zIndex: 9999
    }
})

app.component('Icon', Icon)

app.mount('#app')
