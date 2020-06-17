import Vue from 'vue'
import Router from 'vue-router'
import store from './vuex'

Vue.use(Router)

/* eslint-disable */
let router =  new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: '/home',
      name: 'home',
      component: () => import('@/routes/Overview/Overview.vue')
    },
    {
      path: '/webnetter',
      name: 'webnetter',
      component: () => import('@/routes/Webnetter/Webnetter.vue')
    }
  ]
})
export default router