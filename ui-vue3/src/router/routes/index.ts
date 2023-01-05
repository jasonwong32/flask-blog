import type { RouteRecordRaw } from 'vue-router'

/**
 * 路由配置
 * @description 所有路由都在这里集中管理
 */
const routes: RouteRecordRaw[] = [
  /**
   * 首页
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
  /**
   * 子路由示例
   */
  {
    path: '/foo',
    name: 'foo',
    component: () =>
      import(/* webpackChunkName: "foo" */ '@cp/TransferStation.vue'),
    meta: {
      title: 'Foo',
    },
    redirect: {
      name: 'bar',
    },
    children: [
      {
        path: 'bar',
        name: 'bar',
        component: () =>
          import(/* webpackChunkName: "bar" */ '@views/foo/bar.vue'),
        meta: {
          title: 'Bar',
        },
      },
    ],
  },
]

export default routes
