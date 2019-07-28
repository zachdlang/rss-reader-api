import Vuex from 'vuex';
import Vue from 'vue';
import axios from 'axios';

Vue.use(Vuex);

export const AUTH_LOGIN = 'AUTH_LOGIN';
export const AUTH_SUCCESS = 'AUTH_SUCCESS';
export const AUTH_ERROR = 'AUTH_ERROR';

export default new Vuex.Store({
  state: {
    token: localStorage.getItem('user-token') || '',
    status: '',
  },
  getters: {
    isAuthenticated: state => !!state.token,
    authStatus: state => state.status,
  },
  mutations: {
    [AUTH_LOGIN]: (state) => {
      state.status = 'loading'; // eslint-disable-line no-param-reassign
    },
    [AUTH_SUCCESS]: (state, token) => {
      state.status = 'success'; // eslint-disable-line no-param-reassign
      state.token = token; // eslint-disable-line no-param-reassign
    },
    [AUTH_ERROR]: (state) => {
      state.status = 'error'; // eslint-disable-line no-param-reassign
    },
  },
  actions: {
    [AUTH_LOGIN]: ({ commit, dispatch }, user) => { // eslint-disable-line arrow-body-style
      return new Promise((resolve, reject) => {
        commit(AUTH_LOGIN);
        axios({ url: '/login', data: user, method: 'POST' })
          .then((resp) => {
            const { token } = resp.data;
            localStorage.setItem('user-token', token);
            axios.defaults.headers.common.Authorization = token;
            commit(AUTH_SUCCESS, token);
            resolve(resp);
          })
          .catch((error) => {
            commit(AUTH_ERROR, error);
            localStorage.removeItem('user-token');
            reject(error);
          });
      });
    },
  },
});
