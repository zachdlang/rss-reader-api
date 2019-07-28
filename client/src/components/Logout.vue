<template>
  <div>
  </div>
</template>

<script>

export default {
  name: 'Logout',
  methods: {
    logout() {
      localStorage.removeItem('user-token');
      this.$router.push('/login');
    },
  },
  created() {
    this.logout();
  },
};
</script>
