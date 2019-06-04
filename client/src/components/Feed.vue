<template>
  <div>
    <table>
      <thead>
        <tr>
          <th>&nbsp;</th>
          <th>Name</th>
          <th>Description</th>
          <th>Date</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="article in articles" v-bind:key="article.guid">
          <td><img :src="article.image"></td>
          <td>{{ article.title }}</td>
          <td>{{ article.description }}</td>
          <td>{{ article.published }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Feed',
  data() {
    return {
      articles: [],
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/api/feeds';
      axios.get(path)
        .then((resp) => {
          this.articles = resp.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
};
</script>
