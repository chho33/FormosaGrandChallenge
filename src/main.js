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

VueCookies.config('1d')
Vue.config.productionTip = false
Vue.use(uploader)
Vue.use(Vuetify)
Vue.use(VueCookies)
Vue.use(Vuex)

// Vue.use(VueRouter)

const store = new Vuex.Store({
  state: {
    fileType: ''
  },
  mutations: {
    updateFileType (state, setType) { state.fileType = setType}
  }
});

const vue = new Vue({
  router,
  store,
  computed: mapState([
    'fileType'
  ]),
  render: h => h(App)
})

vue.$mount('#app')
