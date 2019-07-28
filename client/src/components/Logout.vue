<template>
  <div>
  </div>
</template>

<script>
import { AUTH_LOGOUT } from '../store/store';

export default {
  name: 'Logout',
  methods: {
    logout() {
      commit(AUTH_LOGOUT);
      localStorage.removeItem('user-token');
      this.$router.push('/login');
    },
  },
  created() {
    this.logout();
  },
};
</script>
