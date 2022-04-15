import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './vuex'
import vuetify from './plugins/vuetify'


Vue.config.productionTip = false



// COMPONENTS
import menu from '@/components/Common/BaseCard.vue'
Vue.component('BaseCard', menu)

import BaseTable from '@/components/Common/BaseTable.vue'
Vue.component('BaseTable', BaseTable)

import runCommandsTab1 from '@/routes/Webnetter/runCommands/tab1.vue'
Vue.component('runCommandsTab1', runCommandsTab1)

import configureTab2 from '@/routes/Webnetter/configure/tab2.vue'
Vue.component('configureTab2', configureTab2)

import scpTab3 from '@/routes/Webnetter/scp/tab3.vue'
Vue.component('scpTab3', scpTab3)

Vue.use(require('vue-moment'))

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
