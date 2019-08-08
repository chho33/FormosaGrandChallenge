import Vue from 'vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import 'vuetify/src/stylus/app.styl'
import uploader from 'vue-simple-uploader'
import VueCookies from 'vue-cookies'
import Vuex from 'vuex'
import { mapState } from 'vuex'

import App from '@/App.vue'

//import store from '@/store' 
import router from '@/router'
import * as CONFIG from './config.json'
const host = CONFIG.host

VueCookies.config('1d')
Vue.config.productionTip = false
Vue.use(uploader)
Vue.use(Vuetify)
Vue.use(VueCookies)
Vue.use(Vuex)

// Vue.use(VueRouter)

const store = new Vuex.Store({
  state: {
    fileType: '',
    context: '',
    question: '',
    choices: '',
    answer: '',
    host: host,
  },
  getters: {
  },
  mutations: {
    updateFileType (state, setType) { state.fileType = setType },
    fillText (state, payload) { state[payload.tabType] = payload.text },
  }
});

const vue = new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})

//vue.$mount('#app')
