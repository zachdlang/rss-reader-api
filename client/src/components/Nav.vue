<template>
  <div id="navButtons">
    <a class="button is-light" v-if="this.authenticated" href="/logout">
      Log Out
    </a>
  </div>
</template>

<script>
export default {
  name: 'Nav',
  computed: {
    authenticated() { return this.$store.getters.isAuthenticated; },
  },
};
</script>
