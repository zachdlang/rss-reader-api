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
      this.$store.dispatch(AUTH_LOGOUT)
        .then(() => {
          this.$router.push('/login');
        });
    },
  },
  created() {
    this.logout();
  },
};
</script>
