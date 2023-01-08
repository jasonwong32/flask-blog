import type { RouteRecordRaw } from 'vue-router'

/**
 * router configuration
 * @description manage all the routers
 */
const routes: RouteRecordRaw[] = [
  /**
   * home page
   */
  {
    path: '/',
    name: 'home',
    component: () => import(/* webpackChunkName: "home" */ '@views/home.vue'),
    meta: {
      title: 'Home',
    },
  },
  {
    path: '/user/login',
    name: 'login',
    component: () => import('@views/user/login.vue'),
    meta: {
      title: 'Sign in',
    },
  },
  {
    path: '/user/signup',
    name: 'signup',
    component: () => import('@views/user/signup.vue'),
    meta: {
      title: 'Welcome sign up',
    },
  },
]

export default routes
