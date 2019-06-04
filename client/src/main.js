import Vue from 'vue';
import axios from 'axios';
import App from './App.vue';
import router from './router';
import store from './store/store';
import 'bulma/css/bulma.css';

Vue.config.productionTip = false;

const token = localStorage.getItem('user-token');
if (token && token !== 'undefined') {
  axios.defaults.headers.common.Authorization = token;
}


new Vue({
  router,
  store,
  render: h => h(App),
  created() {
    axios.interceptors.response.use(response => response,
      (error) => { // eslint-disable-line arrow-body-style
        return new Promise((resolve, reject) => { // eslint-disable-line no-unused-vars
          /* eslint no-underscore-dangle: ["error", { "allow": ["__isRetryRequest"] }] */
          if (error.response.status === 401) {
            this.$router.push('/login');
          }
          throw error;
        });
      });
  },
}).$mount('#app');
