<template>
  <div>
    <form class="login" @submit.prevent="login">
      <h1 class="title">Login</h1>
      <div class="field">
        <div class="control has-icons-left">
          <input required v-model="username" type="text" class="input" placeholder="Username" />
          <span class="icon is-small is-left">
            <i class="fas fa-envelope"></i>
          </span>
        </div>
      </div>
      <div class="field">
        <div class="control has-icons-left">
          <input required v-model="password" type="password" class="input" placeholder="Password" />
          <span class="icon is-small is-left">
            <i class="fas fa-lock"></i>
          </span>
        </div>
      </div>
      <hr/>
      <div class="field">
        <div class="control">
          <button class="button is-success" type="submit">Login</button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import { AUTH_REQUEST } from '../store/store';

export default {
  name: 'Login',
  props: {
    username: String,
    password: String,
  },
  methods: {
    login() {
      const { username, password } = this;
      this.$store.dispatch(AUTH_REQUEST, { username, password })
        .then(() => {
          this.$router.push('/');
        });
    },
  },
};
</script>
