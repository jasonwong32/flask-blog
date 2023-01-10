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
  {
    path: '/user/reset/password',
    name: 'reset',
    component: () => import('@views/user/resetpasswd.vue'),
    meta: {
      title: 'Reset password',
    },
  },
  {
    path: '/user/signup/success',
    name: 'signupsuccess',
    component:()=>import('@views/user/signupsuccess.vue'),
    meta: {
      title: 'Signup successful',
    }
  }
]

export default routes
