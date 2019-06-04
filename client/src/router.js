import Vue from 'vue';
import Router from 'vue-router';
import store from './store/store';
import Login from './components/Login.vue';
import Logout from './components/Logout.vue';
import Feed from './components/Feed.vue';

Vue.use(Router);

const ifNotAuthenticated = (to, from, next) => {
  if (!store.getters.isAuthenticated) {
    next();
    return;
  }
  next('/');
};

const ifAuthenticated = (to, from, next) => {
  if (store.getters.isAuthenticated) {
    next();
    return;
  }
  next('/login');
};

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login,
      beforeEnter: ifNotAuthenticated,
    },
    {
      path: '/logout',
      name: 'Logout',
      component: Logout,
    },
    {
      path: '/',
      name: 'Feed',
      component: Feed,
      beforeEnter: ifAuthenticated,
    },
    {
      path: '/feed',
      name: 'Feed',
      component: Feed,
      beforeEnter: ifAuthenticated,
    },
  ],
});
