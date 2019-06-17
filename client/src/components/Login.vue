<template>
  <div>
    <FlashMessage></FlashMessage>
    <form class="login" @submit.prevent="login">
      <h1 class="title">Login</h1>
      <div class="field">
        <div class="control has-icons-left">
          <input required type="text" class="input" placeholder="Username"
            @change="setUsername(username)" />
          <span class="icon is-small is-left">
            <i class="fas fa-envelope"></i>
          </span>
        </div>
      </div>
      <div class="field">
        <div class="control has-icons-left">
          <input required type="password" class="input" placeholder="Password"
            @change="setPassword(password)" />
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
        })
        .catch((error) => {
          if (error.response.status === 401) {
            this.flashMessage.show({
              status: 'error',
              title: 'Login unsuccessful.',
              message: 'Please check your credentials.',
              clickable: false,
              icon: `${process.env.BASE_URL}error-triangle.png`,
              iconClass: 'image is-96x96',
            });
          }
        });
    },
    setUsername(username) {
      this.username = username;
    },
    setPassword(password) {
      this.password = password;
    },
  },
};
</script>
