import { createApp } from 'vue'
import App from './App.vue'

import BootstrapVue3 from 'bootstrap-vue-3'

// Optional, since every component import their Bootstrap functionality
// the following line is not necessary
// import 'bootstrap'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'
import mitt from 'mitt';
const emitter = mitt();
const app = createApp(App);
app.config.globalProperties.emitter = emitter
app.use(BootstrapVue3)
app.mount('#app')

