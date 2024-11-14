import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { QuillEditor } from '@vueup/vue-quill'
import VIdle from 'v-idle';
import '@vueup/vue-quill/dist/vue-quill.snow.css';
// OR | AND
import '@vueup/vue-quill/dist/vue-quill.bubble.css';
// you can use both themes at the same time and use them interchangeably
import vuetify from './plugins/vuetify';
import 'vue-toast-notification/dist/theme-default.css';
import ToastPlugin from 'vue-toast-notification';

const app = createApp(App);
app.use(router);
app.component('QuillEditor', QuillEditor);
app.component('VIdle', VIdle);
app.use(ToastPlugin);
app.use(vuetify);
app.mount('#app');