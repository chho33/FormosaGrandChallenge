import Vue from 'vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import 'vuetify/src/stylus/app.styl'

import uploader from 'vue-simple-uploader'

import App from '@/App.vue'

import store from '@/store' 
import router from '@/router'

Vue.config.productionTip = false
Vue.use(uploader)
Vue.use(Vuetify)

// Vue.use(VueRouter)

const vue = new Vue({
  router,
  store,
  render: h => h(App)
})

vue.$mount('#app')
